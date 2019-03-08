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

        # Monte Carlo Sampling
        self.sample_children()

        # Display Results
        print(f'======== FINAL PAYOFF TABLE ({self.row}x{self.col}) ========')
        for payoff in self.payoff_table:
            print(payoff)
        for payoff in self.payoff_table:
            for p in payoff:
                p.display_sample()

    def initialize_table(self):
        """
        Initialize payoff table with specified dimensions
        """
        self.row = len(self.children)
        self.col = self.row - 1

        # initialize table to contain all of the samples
        self.payoff_table = [[None] * self.col for sample in range(self.row)]

    def sample_children(self):
        # TODO: rename variables and adjust comments so they make more sense
        row = 0
        col = 0

        # go through all of player 1's legal moves
        for child, piece, p1_position, legal_positions in self.children:
            moves_remain = True
            payoff = (-1, -1 , -1)
            other_piece = self.other_player(piece)
            _, winner = child.winning_state(piece, p1_position)

            if len(legal_positions) < 1 or winner == 0 or winner == 1:
                moves_remain = False
                payoff = self.monte_carlo_sampling(child, piece, p1_position, moves_remain=moves_remain)
                print(f'FIRST PLAYER\'s payoff: {payoff} and Board State:')
                child.display()

                # if a winner exists, run sampling with True Boolean to indicate no more legal moves remain
                if winner == 0 or winner == 1:
                    print(f'GAME ENDED: Winner Found')
                    for col in range(self.col):
                        self.payoff_table[row][col] = Sample(deepcopy(child.state), piece, other_piece,
                                                             p1_position, legal_positions[col], payoff)
                else:
                # if the board is full, run sampling with True Boolean to indicate no more legal moves remain
                    print(f'GAME ENDED: Full Board')
                    for col in range(self.col):
                        self.payoff_table[row][col] = Sample(deepcopy(child.state), piece, other_piece,
                                                             p1_position, nan, payoff)

                # TODO: Test display
                print(f'PAYOFF TABLE row: {row}, col: {col}')
                self.payoff_table[row][col].display_sample()
                continue

            # If valid moves remain, go through all of them to represent player 2's reponses
            if moves_remain:
                print(f'FIRST PLAYER\'s payoff: {payoff} and Board State (continuing to second player)')
                child.display()

                for p2_position in range(self.col):
                    sample_board = Board(deepcopy(child.state), child.move_count, child.current_player, child=True)
                    _, winner = sample_board.add_piece(other_piece, position=legal_positions[p2_position])

                    # process game_state and winner values and get sample values
                    print(f'\nSECOND PLAYER\'s payoff: {payoff} and Board State')
                    sample_board.display()

                    # start sampling
                    payoff = self.monte_carlo_sampling(sample_board, other_piece, p2_position)

                    # save the Sample to the specific coordinate it belongs to in the payoff table
                    self.payoff_table[row][col] = Sample(deepcopy(sample_board.state), piece, other_piece, p1_position,
                                                         legal_positions[p2_position], payoff)
                    print(f'PAYOFF TABLE row: {row}, col: {col}')
                    self.payoff_table[row][col].display_sample()
                    col += 1
                    if col == self.col:
                        col = 0
            row += 1

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

    def monte_carlo_sampling(self, state: Board, piece: int, position: int, moves_remain: bool=True) -> (int, int, int):
        """
        Sample from board state a constant number of times
        :param state: the current state to sample
        :param piece: most recent piece added
        :param position: where most recent piece was added
        :param moves_remain: True if there are more legal moves in the current board, False otherwise
        :return: payoff values for current state
        """
        payoff = (-1, -1, -1)

        # if there were no legal moves after player 1 placed its piece
        if not moves_remain:
            print(f'NO LEGAL MOVES after PLAYER ONE placed its piece')
            _, winner = state.winning_state(piece, position)
            return self.game_state(winner)

        # if there were no legal moves after player 2 placed its piece
        # check for stalemate, winners
        if state.legal_move() == -1:
            print(f'NO LEGAL MOVES after PLAYER TWO placed its piece')
            _, winner = state.winning_state(piece, position)
            return self.game_state(winner)

        # TODO: run game SAMPLE number of times while collecting (O won, X won, stalemate)
        print(f'RUN MCMC SAMPLING because legal moves remain')
        return nan, nan, nan # TODO update

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

    def get_state(self) -> [int]:
        """
        :return: returns the board's current state
        """
        return self.state


    def create_payoff_table(self):
        """
        Samples from the starting board state to generate a (0, 1, -1, -2) probability out of a total constant sampling
        where the returned result reflects (Number of times O won, Number of times X won, Stalemates)
        off of the next two possible moves in the game.
        """

        # if there are no children
        if len(self.children) < 1:
            return (0, 0, 0)

        # sample each child and save the probabilities
        for child in self.children:
            payoff = self.monte_carlo_sampling(child)
            self.payoff_table.append(payoff)

    def display_payoff_table(self):
        """
        Displays payoff table
        """
        print(f'PAYOFF TABLE:\n{self.payoff_table}')
