from sample import Sample
from tabulate import tabulate
import numpy as np

class Table:

    def __init__(self, player_order: [int], legal_positions: [int], payoff_table: [Sample]):
        """
        :param player_order: which player goes first/second (first player's strategies are listed in left-hand
        column, and second player's strategy is listed on first row)
        :param legal_positions: all of the legal positions remaining
        :param payoff_table: payoff table with strategies played, payoff values from monte carlo sampling, and game state
        """
        self.first_player, self.second_player = self.represent_players(player_order)
        self.legal_positions = legal_positions
        self.payoff_table = payoff_table
        self.y_axis_length = len(self.legal_positions)
        self.x_axis_length = self.y_axis_length - 1

    def display_table(self):
        """
        Displays the entire Payoff Table in a human-readable format
        """
        for payoff in payoff_matrix:
            print(payoff)

    def create_human_readable_table(self):
        """
        Creates the entire Payoff Table in a human-readable format
        """
        payoff_matrix = [[None] * 9 for sample in range(9)]

        for payoff in self.payoff_table:
            for p in payoff:
                p1, p2 = p.get_strategy()
                payoff_matrix[p1][p2] = p.get_payoff()

    def represent_players(self, player_order) -> str:
        """
        Returns the pieces that represent each player
        :param player_order: the first and second player's values
        :return the first player's pice, the second player's piece (e.g. X, O)
        """
        players = ['', '']

        for i in range(len(player_order)):
            if player_order[i] == 0:
                players[i] = 'O'
            else:
                players[i] = 'X'

        return players[0], players[1]

