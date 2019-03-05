from board import Board

class Game:

    def __init__(self):
        self.play = True
        self.board = Board()
        self.board.random_board()
        self.max_player = 0
        self.min_player = 1
        self.current_player = 0
        self.players = [self.max_player, self.min_player]
        self.winner = None

    def running(self, playing: bool=True) -> bool:
        """
        If a parameter is passed to end game, the game is ended. Otherwise, a check is made to see if the game has ended.
        :param playing: False if game has ended, True if not ended or default parameter value is used
        """
        if not playing or self.board.legal_move() < 0:
            print(f'GAME OVER!')
            self.play = False
        return self.play

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
        result = self.board.add_piece(self.players[self.current_player], position)

        if result == 0:
            self.running(False)

        return result

    def display(self):
        """
        Display the board
        """
        self.board.display_flat()
        self.board.display()

    def switch_player(self):
        """
        Switch to the other player
        """
        if self.current_player == 0:
            self.current_player = 1
        else:
            self.current_player = 0


def main():
    game = Game()
    move = 0
    game.display()

    while game.running() and move < 10:
        move += 1
        print(f'\nMove {move}')

        game.random_move()
        game.switch_player()
        game.display()


if __name__ == '__main__':
    main()

