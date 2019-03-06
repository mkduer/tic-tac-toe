import constant as C
from random import choice
import numpy as np


class Board:

    def __init__(self):
        self.state = np.zeros((C.DIMENSION, C.DIMENSION), dtype=int)
        self.state.fill(-1)
        self.end_game = False
        self.random_board()

    def winning_state(self, last_added: int):
        """
        Checks if the current board state is a winning state
        :return:
        """
        print(f'TODO')

    def add_piece(self, piece: int, position: int) -> int:
        """
        Adds a piece to the board if the move is legal. If legal position equals -1, there are no more legal moves,
        if it equals 9, a random position can be chosen, if it equals a value between [0, 8], the piece can
        be added to that position.
        :param piece: piece to add
        :param position: position in which to add the piece
        :return 1 if successfully added, 0 otherwise
        """
        legal_position = self.legal_move(position)

        # no legal positions are available
        if legal_position == -1:
            return 0

        # add piece to position
        self.state.ravel()[position] = piece
        self.display_flat()
        return 1

    def random_legal_move(self) -> int:
        """
        Generates a random legal move if there are any remaining
        :return: legal position or -1 if no legal positions remain
        """
        # find legal positions
        positions = np.where(self.state.ravel() < 0)[0]

        if positions.size < 1:
            return -1

        return choice(positions)

    def collect_legal_moves(self) -> (int, int):
        """
        If there are any viable legal moves, their coordinates are returned
        :return: list of coordinates
        """
        legal_moves = np.where(self.state < 0)[0], np.where(self.state < 0)[1]

        # if there are no legal moves remaining, return invalid coordinates
        if legal_moves[0] == []:
            return -1, -1

        # otherwise, return legal coordinates
        return list(zip(legal_moves[0], legal_moves[1]))

    def legal_move(self, position: int=-2) -> int:
        """
        Check if any legal positions remain on the board, or if the specificly stated position is legal
        :param position: a specific position or, by default, an invalid position of -2
        :return: -1 if there are no more legal positions,
                 position [0-8] if the specific position is not legal
                 9 if unspecified legal moves remain
        """
        coordinates = self.collect_legal_moves()

        # if there are no legal moves remaining
        if coordinates == (-1, -1):
            return -1

        # if there are legal moves remaining, but the position wasn't specified
        if position == -2:
            return 9

        # if the position was specified, check if it is a legal move
        self.display_flat()
        if self.state.ravel()[position] == -1:
            return position
        else:
            return -1

    def alternate_piece(self, curent_piece: int) -> int:
        """
        Alternates to the opposite piece
        :param curent_piece: value of current piece: 0 or 1
        :return: alternate piece: 1 or 0
        """
        if not curent_piece:
            return 1
        return 0

    def random_board(self, moves: int=2) -> int:
        """
        Creates a randomly generated, legal board that may be a set number of moves into a game
        :param move: number of moves into the game, defaults to 2 moves
        :return 1 if a random board is successfully created, 0 otherwise
        """
        # if an invalid numbr of moves is selected, the board is not generated
        if moves < 0 or moves > 8:
            return 0

        # create the board, one legal move at a time
        count = 0
        piece = 0
        while count < moves and not self.end_game:
            position = self.random_legal_move()

            if position < 0 or not self.add_piece(piece, position):
                self.end_game = True
                return 0
            self.display_flat()
            self.display()
            count += 1
            piece = self.alternate_piece(piece)
        return 1

    def static_board(self):
        """
        Creates a statically set board: [0, -1, 1, -1, 0, -1, -1, -1, 1]

        O |   | X
        ---------
          | O |
        ---------
          |   | X

        """
        state = [0, -1, 1, -1, 0, -1, -1, -1, 1]
        state_np = np.asarray(state, dtype=int)
        self.state = np.reshape(state_np, (C.DIMENSION, C.DIMENSION))

    def piece(self, value: int) -> str:
        """
        Convert integer value of piece into the string equivalent for the game
         0 ~> 'O'
         1 ~> 'X'
        -2 ~> ' '
        :param value: integer representation of piece
        :return: string representation of piece
        """
        if value < 0:
            return ' '
        if value > 0:
            return 'X'
        return 'O'

    def display(self):
        """
        Displays Tic Tac Toe as a 2-dimesnional standard 3x3 board
        """
        line_break = 0
        for row in self.state:
            print(self.piece(row[0]) + ' | ' +
                  self.piece(row[1]) + ' | ' + \
                  self.piece(row[2]))
            if line_break < 2:
                print('---------')
            line_break += 1

    def display_flat(self):
        """
        Displays Tic Tac Toe as a flat list
        """
        print(f'board: {self.state.ravel()}')
