import constant as C
from random import choice
import numpy as np
from copy import deepcopy


class Board:

    def __init__(self, state: []=None, move: int=0, current_player: int=0, child: bool=False):
        self.state = np.zeros((C.DIMENSION, C.DIMENSION), dtype=int)
        if state is None:
            self.state.fill(-1)
        else:
            self.state = state
        self.move_count = move
        self.current_player = current_player
        self.end_game = False
        self.winning_player = -1

        # set board if specified
        if C.RANDOM and not child:
            self.current_player = self.random_board(C.MOVES)
        elif C.STATIC:
            self.current_player = self.static_board()

        self.children = []      # contains a triplet: (child state,
                                # move that led to child state,
                                # remaining legal positions)

    def discover_children(self) -> []:
        """
        Generates a child state based on a specifc legal move being added to the parent board
        :return all of the child states
        """
        self.children.clear()

        legal_positions = self.collect_legal_positions()
        if len(legal_positions) < 1:
            return

        # TODO: delete after testing
        print(f'PARENT: ')
        self.display()
        for position in legal_positions:
            child = Board(deepcopy(self.state), self.move_count, self.current_player, child=True)
            piece = child.get_current_player()
            child.add_piece(piece=piece, position=position)
            remaining_legal_positions = deepcopy(legal_positions)
            self.children.append((child, position, remaining_legal_positions.remove(position)))

        return self.children

    def get_current_player(self) -> int:
        """
        :return returns the current player
        """
        return self.current_player

    def reset(self) -> int:
        """
        Resets the board state
        :return current player's piece value in order to continue the game
        """
        self.current_player = 0
        self.state.fill(-1)
        self.move_count = 0
        self.end_game = False
        self.winning_player = -1

        # set board if specified
        if C.RANDOM:
            self.current_player = self.random_board(C.MOVES)
        elif C.STATIC:
            self.current_player = self.static_board()

        return self.current_player

    def winning_state(self, piece: int, position: int) -> int:
        """
        Checks if the current board state is a winning state
        :param piece: the piece that was placed (0 or 1)
        :param position: the position of the last added piece
        :return: player's piece (0 or 1) if player won, -1 if game was not won,
        """
        x, y = np.unravel_index(position, (C.DIMENSION, C.DIMENSION))

        # check if the entire column has the same pieces
        if self.state[0][y] == piece and self.state[1][y] == piece and self.state[2][y] == piece:
            self.winning_player = piece

        # check if the entire row has the same pieces
        elif self.state[x][0] == piece and self.state[x][1] == piece and self.state[x][2] == piece:
            self.winning_player = piece

        # check diagonal
        elif self.state[0][0] == piece and self.state[1][1] == piece and self.state[2][2] == piece:
            self.winning_player = piece

        # check other diagonal
        elif self.state[0][2] == piece and self.state[1][1] == piece and self.state[2][0] == piece:
            self.winning_player = piece

        # check if player won or game continues
        if self.winning_player == piece:
            self.end_game = True
            return piece
        return -1

    def add_piece(self, piece: int, position: int) -> (int, int):
        """
        Adds a piece to the board if the move is legal. If legal position equals -1, there are no more legal moves,
        if it equals 9, a random position can be chosen, if it equals a value between [0, 8], the piece can
        be added to that position.
        :param piece: piece to add
        :param position: position in which to add the piece
        :return tuple (0, -1) if the game was stalemate,
                tuple (1, player_piece) if won,
                tuple (1, 2) if game is continuing
        """
        self.current_player = piece
        legal_position = self.legal_move(position)

        # no legal positions are available
        if legal_position == -1:
            return 0, -1

        # add piece to position
        self.state.ravel()[position] = piece
        return 1, self.winning_state(piece, position)

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

    def collect_legal_positions(self) -> [int]:
        """
        If there are any viable legal moves, their positions are returned
        :return: list of legal positions
        """
        coordinates = self.collect_legal_coordinates()
        positions = []

        if coordinates == (-1, -1):
            return positions

        for coord in coordinates:
            pos = 0
            if coord[0] == 0:
                if coord[1] == 0:
                    pos = 0
                elif coord[1] == 1:
                    pos = 1
                else:
                    pos = 2
            elif coord[0] == 1:
                if coord[1] == 0:
                    pos = 3
                elif coord[1] == 1:
                    pos = 4
                else:
                    pos = 5
            elif coord[0] == 2:
                if coord[1] == 0:
                    pos = 6
                elif coord[1] == 1:
                    pos = 7
                else:
                    pos = 8
            positions.append(pos)
        return positions

    def collect_legal_coordinates(self) -> (int, int):
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
        coordinates = self.collect_legal_coordinates()

        # if there are no legal moves remaining
        if coordinates == (-1, -1):
            return -1

        # if there are legal moves remaining, but the position wasn't specified
        if position == -2:
            return 9

        # if the position was specified, check if it is a legal move
        if self.state.ravel()[position] == -1:
            return position
        else:
            return -1

    def alternate_player(self, current_piece: int) -> int:
        """
        Alternates to the opposite piece
        :param current_piece: value of current piece: 0 or 1
        :return: alternate piece: 1 or 0
        """
        if not current_piece:
            self.current_player = 1
        else:
            self.current_player = 0
        return self.current_player

    def random_board(self, moves: int=2) -> int:
        """
        Creates a randomly generated, legal board that may be a set number of moves into a game
        :param move: number of moves into the game, defaults to 2 moves
        :return 1 if a random board is successfully created, 0 otherwise
        """
        count = 0

        # if an invalid numbr of moves is selected, the board is not generated
        if moves < 0 or moves > 8:
            return 0

        # create the board, one legal move at a time
        piece = 0
        while count < moves and not self.end_game:
            count += 1
            position = self.random_legal_move()
            successful, _ = self.add_piece(piece, position)
            piece = self.alternate_player(piece)

            # if a winning state was reached or the position was not successfully placed
            # reset the game state and continue the while loop to create game state
            if position < 0 or not successful or self.winning_player != -1:
                count = 0
                self.state.fill(-1)
                piece = 0

        return 1

    def static_board(self) -> int:
        """
        Creates a statically set board: [0, -1, 1, -1, 0, -1, -1, -1, 1]

                  O |   | X
                  ---------
        Board~>     | O |
                  ---------
                    |   | X

        :return next player in game, which should always be 0 assuming traditional game play
        """
        state = [0, -1, 1, -1, 0, -1, -1, -1, 1]
        state_np = np.asarray(state, dtype=int)
        self.state = np.reshape(state_np, (C.DIMENSION, C.DIMENSION))
        return 0

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
        print('\n')

    def display_flat(self):
        """
        Displays Tic Tac Toe as a flat list
        """
        print(f'board: {self.state.ravel()}')
