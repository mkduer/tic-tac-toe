from board import Board


class Sample:

    def __init__(self, board: Board, payoff: [(int, int, int)], player1: int, player2: int,
                 p1_position: int, p2_position: int):
        self.strategy = board       # board state as the sample strategy
        self.payoff = payoff        # payoff probability from sampling (O won, X won, stalemate)
        self.player1 = player1
        self.player2 = player2
        self.p1_position = p1_position
        self.p2_position = p2_position

