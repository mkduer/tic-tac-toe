import constant as C
from board import Board
from copy import deepcopy
from sample import Sample
from math import nan
from table import Table
import numpy as np

class Strategy:

    def __init__(self, root: Board):
        self.root = root
        self.children = []
        self.payoff_table = []
        self.row = 0
        self.col = 0
        self.first_player = -1
        self.second_player = -1
        self.original_legal_positions = []
        self.player1_strategies = np.full((1, C.TOTAL_STRATEGIES), -1, dtype=int).ravel()
        self.player2_strategies = np.full((1, C.TOTAL_STRATEGIES), -1, dtype=int).ravel()

    def process(self):
        """
        Processes valid game states for sampling and creating a payoff table.
        """

        # Gather the root state's children
        self.children = self.find_children(self.root)

        # Initialize the payoff table
        self.initialize_table()

        # Monte Carlo Sampling
        self.process_children()

    def dominant_strategies(self):
        """
        Prints whether any dominant strategies exist for either player
        """
        p1_dominant_strategies = []
        p2_dominant_strategies = []

        # discover if any players have a dominant strategy
        for strategy in range(C.TOTAL_STRATEGIES):
            if self.player1_strategies[strategy] == 1:
                p1_dominant_strategies.append(strategy)
            elif self.player2_strategies[strategy] == 1:
                p2_dominant_strategies.append(strategy)

        # display dominant strategies
        print('\nDOMINANT STRATEGIES: ')
        print(f'PLAYER {self.piece(self.first_player)}\'s strategies: {p1_dominant_strategies}')
        print(f'PLAYER {self.piece(self.second_player)}\'s strategies: {p2_dominant_strategies}\n')

    def compare_strategies(self):
        """
        Compares winning and stalemate outcomes based on sampling, defining if a strategy is dominant for a player
        """

        for payoff in self.payoff_table:
            for p in payoff:
                p1, p2, stalemate = p.get_payoff()
                p1_strategy, p2_strategy = p.get_strategy()

                # if p2's strategy consists of nan, then p1 already won and p2 has no dominant strategy
                if type(p2_strategy) != int:
                    for move in self.original_legal_positions:
                        self.player2_strategies[move] = 0

                # if p2 has a better strategy than p1, p1 has no dominant strategy
                else:
                    if p2 > p1:
                        self.player1_strategies[p1_strategy] = 0
                        if self.player2_strategies[p1_strategy] != 0:
                            self.player2_strategies[p1_strategy] = 1

                    # check if stalemate is equal to or exceeds p2
                    if stalemate >= p2:
                        self.player2_strategies[p2_strategy] = 0

                # check if stalemate is equal to or exceeds p1
                if stalemate >= p1:
                    self.player1_strategies[p1_strategy] = 0

                # if p1 has a better strategy than p2, p2 has no dominant strategy
                elif p1 > p2:
                    if self.player1_strategies[p1_strategy] != 0:
                        self.player1_strategies[p1_strategy] = 1

                    # if p2 is a nan, it means that player1 already won
                    # so set all of those strategy outcomes as non-dominant
                    if type(p2_strategy) != int:
                        for move in self.original_legal_positions:
                            self.player2_strategies[move] = 0

                    # otherwise, just set the specific strategy as non-dominant
                    else:
                        self.player2_strategies[p2_strategy] = 0

    @staticmethod
    def piece(value: int) -> str:
        """
        Convert integer value of piece into the string equivalent for the game
         0 ~> 'X'
         1 ~> 'O'
        -2 ~> ' '
        :param value: integer representation of piece
        :return: string representation of piece
        """
        if value < 0:
            return ' '
        if value > 0:
            return 'O'
        return 'X'

    def initialize_table(self):
        """
        Initialize payoff table with specified dimensions
        """
        self.row = len(self.children)
        self.col = self.row - 1

        # initialize table to contain all of the samples
        self.payoff_table = [[None] * self.col for sample in range(self.row)]

    def process_children(self):
        """
        Processes each child to see if its board still has legal moves remaining. If not, the payoff is set.
        If legal moves remain, the children's children are processed. If an end game state is not encountered,
        the boards are run with monte carlo sampling and their payoff values are decided. The strategy combinations
        and payoffs are saved in the payoff table.
        """
        player1 = 0
        player2 = 0
        original_positions = True

        # go through all of player 1's legal moves
        for board, self.first_player, p1_position, legal_positions in self.children:
            if original_positions:
                self.original_legal_positions = deepcopy(legal_positions)
                self.original_legal_positions.append(p1_position)
                no_moves = False

            moves_remain = True
            payoff = (-1, -1 , -1)
            self.second_player = self.other_player(self.first_player)
            _, winner = board.winning_state(self.first_player, p1_position)

            # if a stalemate is encountered or a winner exists,
            # run sampling with True Boolean to indicate no more legal moves remain
            if len(legal_positions) < 1 or winner == 0 or winner == 1:
                moves_remain = False
                payoff = self.monte_carlo_sampling(board, self.first_player, p1_position, moves_remain=moves_remain)

                for col in range(self.col):
                    self.payoff_table[player1][col] = Sample(deepcopy(board.state), self.first_player, self.second_player,
                                                         p1_position, nan, deepcopy(payoff))

            # If valid moves remain, go through all of them to represent player 2's reponses
            if moves_remain:
                for position in range(self.col):
                    moves_remain = True
                    sample_board = Board(deepcopy(board.state), board.move_count, board.current_player, child=True)
                    _, winner = sample_board.add_piece(self.second_player, position=legal_positions[position])

                    if winner == 0 or winner == 1:
                        moves_remain = False
                        payoff = self.monte_carlo_sampling(sample_board, self.second_player, legal_positions[position],
                                                           moves_remain=moves_remain)
                    # start sampling
                    if moves_remain:
                        payoff = self.monte_carlo_sampling(sample_board, self.second_player, legal_positions[position])

                    # save the Sample to the specific coordinate it belongs to in the payoff table
                    self.payoff_table[player1][player2] = Sample(deepcopy(sample_board.state), self.first_player,
                                                                 self.second_player, p1_position,
                                                                 legal_positions[position], deepcopy(payoff))

                    # set payoff table location according to relevant players
                    player2 += 1
                    if player2 == self.col:
                        player2 = 0

            player1 += 1

    def monte_carlo_sampling(self, board: Board, piece: int, position: int, moves_remain: bool=True) -> (int, int, int):
        """
        Sample from board state a constant number of times
        :param board: the current board to sample
        :param piece: most recent piece added
        :param position: where most recent piece was added
        :param moves_remain: True if there are more legal moves in the current board, False otherwise
        :return: payoff values for current board
        """
        # if there were no legal moves after player 1 placed its piece
        if not moves_remain:
            _, winner = board.winning_state(piece, position)
            return self.game_state(winner)

        # run game SAMPLE number of times while collecting (p1 won, p2 won, stalemate) samples
        count = 0
        p1_total = 0
        p2_total = 0
        stalemates = 0

        if C.SAMPLES < 0:
            raise ValueError(f'SAMPLES constant in constant.py must be within [0, 999] inclusive.')

        while count < C.SAMPLES:
            p1_won, p2_won, no_win = self.sample_run(deepcopy(board))
            if (p1_won, p2_won, no_win) == (-1, -1, -1):
                raise ValueError('An error occurred with the gameplay. These values should not be returned')
            p1_total += p1_won
            p2_total += p2_won
            stalemates += no_win
            count += 1
        return p1_total, p2_total, stalemates

    def sample_run(self, board: Board) -> (int, int, int):
        """
        Uses the provided board state to start a sample run and continues until an end state is reached.
        The end result concluding whether O won, X won, or stalemate was reached is returned
        :param board: the current game board
        :return: An integer 1 representing whether there was a win or stalemate, zeros for all other possible outcomes
                 A triplet of (-1, -1, -1) is returned if there was an error in the gameplay
        """
        end_game = False

        # run the game until an endgame is reached
        while not end_game:
            position = board.random_legal_move()
            player = board.get_current_player()
            player = board.alternate_player(player)
            _, winner = board.add_piece(player, position)
            if winner == -1:
                end_game = True
                return 0, 0, 1  # stalemate
            elif winner == 0:
                end_game = True
                return 1, 0, 0  # X won
            elif winner == 1:
                end_game = True
                return 0, 1, 0  # O won

        return -1, -1 ,-1

    def game_state(self, winner: int) -> (int, int, int):
        """
        Returns payoff if board game will no longer change based on winner value
        :param winner: value of winner where O wins all, X wins all, or stalemate
        :return: payoff values
        """
        if winner == 0:
            return (C.SAMPLES, 0, 0)
        if winner == 1:
            return (0, C.SAMPLES, 0)
        return (0, 0, C.SAMPLES)

    def other_player(self, piece: int) -> int:
        """
        Set the value of player 2's piece inferred from player 1's piece
        :param piece: value of first player's piece
        :return value of second player's piece
        """
        if piece == 0:
            return 1
        return 0

    def find_children(self, board: Board) -> [Board]:
        """
        Finds all possible child states based on the board state
        :param board: current board
        :return A list of children board states stemming out from current board
        """
        return board.discover_children()

    def generate_payoff_table(self) -> [[str]]:
        """
        Generates payoff table
        :return the payoff table
        """
        player_order = (self.first_player, self.second_player)
        table = Table(player_order, self.original_legal_positions, self.payoff_table)
        table.create_human_readable_table()
        table.display_table()
        return table.payoff_table
