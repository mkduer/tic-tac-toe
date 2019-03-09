import constant as C
from board import Board
from copy import deepcopy
from sample import Sample
from math import nan

class Strategy:

    def __init__(self, root: Board):
        self.root = root
        self.children = []
        self.payoff_table = []
        self.row = 0
        self.col = 0

    def analysis(self):
        """
        Runs all of the steps of analysis:
        """

        # Gather the root state's children
        self.children = self.find_children(self.root)

        # Initialize the payoff table
        self.initialize_table()
        print(f'INITIALIZED TABLE:')
        for payoff in self.payoff_table:
            print(payoff)
        print(f'\n')

        # Monte Carlo Sampling
        self.process_children()

        # Display Results in Payoff Table
        self.display_payoff_table()

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

        # go through all of player 1's legal moves
        for board, piece, p1_position, legal_positions in self.children:
            print(f'PLAYER1: {player1}')
            moves_remain = True
            payoff = (-1, -1 , -1)
            other_piece = self.other_player(piece)
            _, winner = board.winning_state(piece, p1_position)

            # if a stalemate is encountered or a winner exists,
            # run sampling with True Boolean to indicate no more legal moves remain
            if len(legal_positions) < 1 or winner == 0 or winner == 1:
                moves_remain = False
                payoff = self.monte_carlo_sampling(board, piece, p1_position, moves_remain=moves_remain)
                print(f'FIRST PLAYER\'s payoff: {payoff} and Board State:')
                board.display()

                for col in range(self.col):
                    print(f'SAMPLE being added to payoff table[{player1}][{col}] with payoff {payoff}')
                    self.payoff_table[player1][col] = Sample(deepcopy(board.state), piece, other_piece,
                                                         p1_position, nan, deepcopy(payoff))

            # If valid moves remain, go through all of them to represent player 2's reponses
            if moves_remain:
                print(f'FIRST PLAYER\'s position {p1_position}, current payoff: {payoff} and'
                      f'\nBoard State (continuing to second player):')
                board.display()

                for position in range(self.col):
                    moves_remain = True
                    print(f'PLAYER2: {player2}')
                    sample_board = Board(deepcopy(board.state), board.move_count, board.current_player, child=True)
                    _, winner = sample_board.add_piece(other_piece, position=legal_positions[position])

                    if winner == 0 or winner == 1:
                        moves_remain = False
                        payoff = self.monte_carlo_sampling(sample_board, other_piece, legal_positions[position],
                                                           moves_remain=moves_remain)
                        print(f'SECOND PLAYER\'s payoff: {payoff} and Board State:')
                        sample_board.display()

                    if moves_remain:
                        # process game_state and winner values and get sample values
                        print(f'\nSECOND PLAYER\'s position {legal_positions[position]}, current payoff: {payoff} and'
                              f'\nBoard State:')
                        sample_board.display()

                        # start sampling
                        payoff = self.monte_carlo_sampling(sample_board, other_piece, legal_positions[position])

                    # save the Sample to the specific coordinate it belongs to in the payoff table
                    print(f'SAMPLE being added to payoff table[{player1}][{player2}] with payoff {payoff}')
                    self.payoff_table[player1][player2] = Sample(deepcopy(sample_board.state), piece, other_piece, p1_position,
                                                         legal_positions[position], deepcopy(payoff))
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
            print(f'NO LEGAL MOVES after PLAYER {piece} placed its piece in position {position}')
            _, winner = board.winning_state(piece, position)
            return self.game_state(winner)

        # run game SAMPLE number of times while collecting (O won, X won, stalemate) samples
        count = 0
        O_total = 0
        X_total = 0
        stalemates = 0
        while count < C.SAMPLES:
            print(f'START mcmc sampling')
            O_won, X_won, no_win = self.sample_run(deepcopy(board))
            if (O_won, X_won, no_win) == (-1, -1, -1):
                assert('An error occurred with the gameplay. These values should not be returned')
            O_total += O_won
            X_total += X_won
            stalemates += no_win
            count += 1
        return O_total, X_total, stalemates

    def sample_run(self, board: Board) -> (int, int, int):
        """
        Uses the provided board state to start a sample run and continues until an end state is reached.
        The end result concluding whether O won, X won, or stalemate was reached is returned
        :param board: the current game board
        :return: An integer 1 representing whether there was a win or stalemate, zeros for all other possible outcomes
                 A triplet of (-1, -1, -1) is returned if there was an error in the gameplay
        """
        print('START SAMPLE RUN with state:')
        board.display()
        end_game = False

        # run the game until an endgame is reached
        while not end_game:
            position = board.random_legal_move()
            player = board.get_current_player()
            player = board.alternate_player(player)
            print(f'player: {player}, position: {position}')
            _, winner = board.add_piece(player, position)
            print(f'new state with winner = {winner}:')
            board.display()
            if winner == -1:
                end_game = True
                print(f'stalemate')
                return 0, 0, 1  # stalemate
            elif winner == 0:
                end_game = True
                print(f'O won')
                return 1, 0, 0  # O won
            elif winner == 1:
                end_game = True
                print(f'X won')
                return 0, 1, 0  # X won
            print(f'Continuing game')

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

    def display_payoff_table(self):
        """
        Displays payoff table
        """
        print(f'======== FINAL PAYOFF TABLE ({self.row}x{self.col}) ========')
        for payoff in self.payoff_table:
            print(payoff)
        for payoff in self.payoff_table:
            for p in payoff:
                if p is None:
                    print(f'FIX ME -- None Value')
                else:
                    p.display_sample()
