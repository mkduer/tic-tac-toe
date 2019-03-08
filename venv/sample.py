from board import Board
from math import nan


class Sample:

    def __init__(self, state: [int], player1: int, player2: int, p1_position: int, p2_position: int,
                 payoff: (int, int, int)):
        self.state = state
        self.player1 = player1
        self.player2 = player2
        self.p1_position = p1_position
        self.p2_position = p2_position
        self.payoff = payoff            # payoff probability from sampling (O won, X won, stalemate)

    def display_sample(self):
        """
        Display sample details
        """
        # TODO: uncomment
        """
        print(f'\nPAYOFF SAMPLE: ({self.piece(self.player1)}, {self.piece(self.player2)}) '
              f'added to ({self.p1_position}, {self.p2_position})')
        self.display_state(self.state)
        """
        print(f'payoff: {self.payoff}')

    def display_state(self, state: [int]):
        """
        Displays Tic Tac Toe as a 2-dimensional standard 3x3 board
        """
        line_break = 0
        for row in state:
            print(self.piece(row[0]) + ' | ' +
                  self.piece(row[1]) + ' | ' + \
                  self.piece(row[2]))
            if line_break < 2:
                print('---------')
            line_break += 1

    @staticmethod
    def piece(value: int) -> str:
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
