from board import Board
from strategy import Strategy
import constant as C
from sample import Sample

class Game:

    def __init__(self):
        self.board = Board()
        self.max_player = 0
        self.min_player = 1
        self.current_player = self.board.get_current_player()
        self.players = [self.max_player, self.min_player]
        self.winner = -1

    def analyze_strategy(self):
        """
        Applies game theory to analyze strategies from the current board state
        """
        strategy = Strategy(self.board)
        payoff_table = strategy.process()
        strategy.analyze()
        strategy.display_payoff_table()

    def reset(self) -> int:
        """
        Resets the game and returns the next player for the new board state
        :return:
        """
        self.current_player = self.board.reset()
        self.winner = -1

    def running(self, playing: bool=True) -> (int, int):
        """
        If a parameter is passed to end game, the game is ended. Otherwise, a check is made to see if the game has ended.
        :param playing: False if game has ended, True if not ended or default parameter value is used
        :return (0, player) if game was won, (-1, -1) if game was stalemated, (1, 1) if game is still running
        """
        if self.winner != -1:
            return 0, self.winner

        if not playing or self.board.legal_move() < 0:
            return -1, -1
        return 1, 1

    def random_move(self) -> int:
        """
        Adds the player's piece to a legal space if one exists
        :return 0 if no more legal moves remain, 1 otherwise
        """
        if self.running():
            position = self.board.random_legal_move()
            return self.move(position)
        return 0

    def move(self, position: int) -> int:
        """
        Adds a specific player's piece to a specific position if it is legal. Checks if game has ended.
        :param position: the board position where the piece will be placed
        :return 1 if successful, 0 if the end of the game has been reached
        """
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

def end_game(reason: int, winner: int):
    """
    Prints end game message
    :param reason: 0 if game was won, -1 if stalemate
    :param winner: 0 or 1 if there was a winner, -1 otherwise
    """
    if reason == 0:
        print(f'====== GAME OVER! ======')
        print(f'Winner is Player {winner}')
        print(f'========================\n')
    else:
        print(f'====== GAME OVER: STALEMATE ======\n')


def main():
    game = Game()
    game_count = 0

    # run total games
    while game_count < C.TOTAL_GAMES:
        if game_count > 0:
            game.reset()

        run_game = 1

        print('\nSTARTING BOARD:')
        game.display()
        print('\n')
        payoff_table = game.analyze_strategy()
        # TODO: display payoff table with only payoffs
        # TODO: display payoff table with all resulting details

        # while the game is running, make moves
        # TODO: uncomment after strategy is implemented
        # TODO: show what actual outcome was compared to suggested strategies
        """
        while run_game > 0:
            if game.random_move() < 0:
                game.running(False)
            game.display()

            run_game, winner = game.running()
            game.switch_player()

        end_game(run_game, winner)
        """
        game_count += 1


if __name__ == '__main__':
    main()

