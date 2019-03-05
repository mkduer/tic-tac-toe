import constant as C
from random import choice
import numpy as np


class Board:

    def __init__(self):
        self.state = np.zeros((C.DIMENSION, C.DIMENSION), dtype=int)
        self.state.fill(-1)

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
        x, y = self.map_position(position)
        print(f'add piece to position {position} found at coordinates {x}, {y}')
        self.state[x][y] = piece
        return 1

    def random_legal_move(self) -> int:
        coordinates = self.collect_legal_moves()

        # if there are no legal moves remaining
        if coordinates == (-1, -1):
            return -1

        # find legal positions
        positions = self.map_coordinates(coordinates)
        if not positions:
            return -1
        print(f'Legal Positions: {positions}')
        return choice(positions)

    def collect_legal_moves(self) -> (int, int):
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
        x, y = self.map_position(position)
        if (x, y) in coordinates:
            return position
        else:
            return -1

    def map_coordinates(self, coordinates: [(int, int)]) -> [int]:
        """
        Maps coordinates over to positions: Example:

        0, 0) | (1, 0) | (2, 0)       0 | 1 | 2
        -----------------------       ---------
        (0, 1) | (1, 1) | (2, 1)  ~>  3 | 4 | 5
        -----------------------       ---------
        (0, 2) | (1, 2) | (2, 2)      6 | 7 | 8

        :param coordinates:
        :return: positions as a list of integers
        """
        positions = []

        if coordinates == []:
            return coordinates

        x, y = zip(*coordinates)
        length = len(x)

        # figure out correlating positions
        for i in range(length):
            if y[i] == 0:
                if x[i] == 0:
                    positions.append(0)
                elif x[i] == 1:
                    positions.append(1)
                else:
                    positions.append(2)
            elif y[i] == 1:
                if x[i] == 0:
                    positions.append(3)
                elif x[i] == 1:
                    positions.append(4)
                else:
                    positions.append(5)
            else:
                if x[i] == 0:
                    positions.append(6)
                elif x[i] == 1:
                    positions.append(7)
                else:
                    positions.append(8)

        return positions

    def map_position(self, position: int) -> (int, int):
        """
        Maps position over to coordinates. Example:

        0 | 1 | 2      (0, 0) | (1, 0) | (2, 0)
        ---------      -----------------------
        3 | 4 | 5  ~>  (0, 1) | (1, 1) | (2, 1)
        ---------      -----------------------
        6 | 7 | 8      (0, 2) | (1, 2) | (2, 2)

        :param position: position to map
        :return: the (x, y) coordinates
        """
        if position == -2:
            raise ValueError(f'{position} is an invalid position on the board and cannot be mapped')
        x = 0
        y = 0
        if -1 < position < 3:
            y = 0
            if position == 0:
                x = 0
            elif position == 1:
                x = 1
            else:
                x = 2
        elif 2 < position < 6:
            if position == 3:
                x = 0
            elif position == 4:
                x = 1
            else:
                x = 2
            y = 1
        else:
            y = 2
            if position == 6:
                x = 0
            elif position == 7:
                x = 1
            else:
                x = 2
        return x, y

    def random_board(self, move: int=2):
        """
        Creates a randomly generated, legal board that is defaulted to at least two moves into the game
        :param move: number of moves into the game
        """
        if move < 1:
            pass
        # TODO

    def static_board(self):
        """
        Creates a statically set board: [O, -2, 1, -2, 0, -2, -2, -2, 1]

        O |   | X
        ---------
          | O |
        ---------
          |   | X

        """
        self.state = [0, -2, 1, -2, 0, -2, -2, -2, 1]

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
