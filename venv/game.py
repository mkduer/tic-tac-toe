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
        strategy.process()
        strategy.compare_strategies()
        payoff_table = strategy.generate_payoff_table()
        strategy.dominant_strategies()
        return payoff_table

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

    def end_game(self, winner: int, payoff_table: [[str]]):
        """
        Prints end game message
        :param winner: an integer value representing the winning piece or stalemate
        """
        if winner < 0:
            print(f'\nGAME OVER: STALEMATE')
        else:
            piece = self.piece(winner)
            print(f'\nGAME OVER: Winner is Player {piece}')

        player1_strategy = self.actual_strategies[0][1]
        print(f'ACTUAL STRATEGIES USED: '
              f'({self.actual_strategies[0][0]}, {player1_strategy})', end='')

        if len(self.actual_strategies) > 1:
            player2_strategy = self.actual_strategies[1][1]
            print(f' and ({self.actual_strategies[1][0]}, {player2_strategy})')
            print(f'Payoff values for the combined strategies ({player1_strategy}, {player2_strategy}): '
                  f'{payoff_table[player1_strategy + 1][player2_strategy + 1]}')
        else:
            print(f'\nSecond player had no valid strategy. Player 1\'s strategy: '
                  f'({player1_strategy}) with payoff (30, 0, 0)')
        print('\n==================================')

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

    print(f'\nSTARTING BOARD ({C.MOVES} moves in):')
    game.display()
    payoff_table = game.analyze_strategy()

    # while the game is running, make moves
    print(f'GAME PLAY:', end='')
    while continue_game > 0:
        if game.random_move() < 0:
            game.running(False)
        else:
            continue_game, winner = game.running()
            game.switch_player()
            print('\n')
            game.display()
    game.end_game(winner, payoff_table)

if __name__ == '__main__':
    main()

