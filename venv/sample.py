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

    def get_strategy(self):
        """
        :return: the tuple of strategies played in order
        """
        return self.p1_position, self.p2_position

    def get_payoff(self):
        return self.payoff

    def display_payoff(self):
        """
        Display payoff details only
        """
        print(self.payoff)
        
    def display_sample(self):
        """
        Display sample details
        """
        print(f'\n({self.piece(self.player1)}, {self.piece(self.player2)}) '
              f'added to ({self.p1_position}, {self.p2_position})'
              f'\npayoff: {self.payoff}')
        self.display_state(self.state)

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
