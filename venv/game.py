from board import Board
from strategy import Strategy
import constant as C
from sample import Sample

class Game:

    def __init__(self):
        self.board = Board()
        self.first_player = 0
        self.second_player = 1
        self.current_player = self.board.get_current_player()
        self.players = [self.first_player, self.second_player]
        self.winner = 2
        self.actual_strategies = []

    def analyze_strategy(self):
        """
        Applies game theory to analyze strategies from the current board state
        """
        strategy = Strategy(self.board)
        payoff_table = strategy.process()
        strategy.compare_strategies()
        strategy.dominant_strategies()
        strategy.display_payoff_table()

    def reset(self) -> int:
        """
        Resets the game and returns the next player for the new board state
        :return:
        """
        self.current_player = self.board.reset()
        self.winner = 2

    def running(self, playing: bool=True) -> (int, int):
        """
        If a parameter is passed to end game, the game is ended. Otherwise, a check is made to see if the game has ended.
        :param playing: False if game has ended, True if not ended or default parameter value is used
        :return (0, player) if game was won, (-1, -1) if game was stalemated, (1, 1) if game is still running
        """
        if self.winner != 2:
            return 0, self.winner

        if not playing or self.board.legal_move() < 0:
            return -1, -1
        return 1, 1

    def random_move(self) -> int:
        """
        Adds the player's piece to a legal space if one exists
        :return 0 if no more legal moves remain, 1 otherwise
        """
        if self.board.legal_move() > -1:
            position = self.board.random_legal_move()
            return self.move(position)
        return 0

    def move(self, position: int) -> int:
        """
        Add a specific player's piece to a specific position if it is legal. Save actual strategies/moves that are made.
        Check if game has ended.
        :param position: the board position where the piece will be placed
        :return 1 if successful, 0 if the end of the game has been reached
        """
        self.actual_strategies.append((self.piece(self.current_player), position))
        result, self.winner = self.board.add_piece(self.players[self.current_player], position)

        if result == 0:
            self.running(False)

        return result

    def display(self):
        """
        Display the board
        """
        # self.board.display_flat() # optional
        self.board.display()

    def switch_player(self):
        """
        Switch to the other player
        """
        if self.current_player == 0:
            self.current_player = 1
        else:
            self.current_player = 0

    def end_game(self, winner: int):
        """
        Prints end game message
        :param winner: an integer value representing the winning piece or stalemate
        """
        print(f'\n==================================')
        print(f'ACTUAL STRATEGY: '
              f'({self.actual_strategies[0][0]}, {self.actual_strategies[0][1]}) and '
              f'({self.actual_strategies[1][0]}, {self.actual_strategies[1][1]})')

        if winner < 0:
            print(f'GAME OVER: STALEMATE')
        else:
            piece = self.piece(winner)
            print(f'GAME OVER: Winner is Player {piece}')
        print('\n')
        self.display()


    def piece(self, value: int) -> str:
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

def main():
    game = Game()
    continue_game = 1

    print('\nSTARTING BOARD:')
    game.display()
    print('\n')
    payoff_table = game.analyze_strategy()

    # while the game is running, make moves
    while continue_game > 0:
        if game.random_move() < 0:
            game.running(False)
        print(f'\n--------------------------')
        game.display()
        continue_game, winner = game.running()
        game.switch_player()
    game.end_game(winner)

if __name__ == '__main__':
    main()

