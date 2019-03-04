from player import Player
import constant as C
from random import choice

class Game:

    def __init__(self):
        self.board = [-1] * C.SIZE
        self.random_board()
        self.legal_moves = list(range(0, C.SIZE))
        self.playing = True

    def playing_game(self, playing: bool=True) -> bool:
        """
        If a parameter is passed to end game, the game is ended. Otherwise, a check is made to see if the game has ended.
        :param playing: False if game has ended, True if not ended or default parameter value is used
        """
        if not playing or not self.legal_moves:
            print(f'GAME OVER!')
            self.playing = False
        return self.playing

    def random_move(self, player: Player):
        """
        Adds the player's piece to a legal space if one exists
        :param player: the player who's piece will be added
        """
        if self.playing_game():
            position = choice(self.legal_moves)
            self.move(player, position)

    def random_board(self, move: int=2):
        """
        Creates a randomly generated, legal board that is defaulted to at least two moves into the game
        :param move: number of moves into the game
        """
        if move < 1:
            pass

    def static_board(self):
        """
        Creates a statically set board: [O, -2, 1, -2, 0, -2, -2, -2, 1]

        O |   | X
        ---------
          | O |
        ---------
          |   | X

        """
        self.board = [0, -2, 1, -2, 0, -2, -2, -2, 1]

    def remove_legal_move(self, position: int):
        """
        Removes a position from legal moves because it is no longer available
        :param position: the position to remove
        """
        del self.legal_moves[position]

    def move(self, player: Player, position: int):
        """
        Adds a specific player's piece to a specific position if it is legal. Checks if game has ended.
        :param player: the player who's piece will be added
        :param position: the board position where the piece will be placed
        :return 1 if successful, -1 if the end of the game has been reached
        """
        # check if any legal moves remain
        loc = self.legal_moves.index(position)
        if loc == None:
            self.playing_game(False)
            return -1

        # add piece and update board and state
        self.board[position] = player.place_piece()
        self.remove_legal_move(loc)

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

    def display_board(self):
        """
        Displays Tic Tac Toe as a 2-dimesnional standard 3x3 board
        """
        length = len(self.board)
        for i in range(0, length, 3):
            print(self.piece(self.board[i]) + ' | ' +
                  self.piece(self.board[i + 1]) + ' | ' + \
                  self.piece(self.board[i + 2]))
            if i < 6:
                print('---------')

    def display_flat(self):
        """
        Displays Tic Tac Toe as a flat list
        """
        print(f'\nboard: {self.board}')

def switch_player(player: int) -> int:
    if player == 0:
        return 1
    return 0


def main():
    game = Game()
    current = 0
    max_player = Player(0)
    min_player = Player(1)
    players = [max_player, min_player]

    move = 0
    game.display_flat()
    game.display_board()

    while game.playing_game():
        move += 1
        game.random_move(players[current])
        current = switch_player((current))
        game.display_flat()
        game.display_board()


if __name__ == '__main__':
    main()

