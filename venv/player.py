class Player:

    def __init__(self, type: int=0):
        self.piece = type  # decides whether the player is X's (MIN) or O's (MAX)

    def place_piece(self) -> int:
        """
        Returns the player's piece
        """
        return self.piece