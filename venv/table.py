from sample import Sample
from tabulate import tabulate
import numpy as np
import constant as C

class Table:

    def __init__(self, player_order: [int], legal_positions: [int], samples: [Sample]):
        """
        :param player_order: which player goes first/second (first player's strategies are listed in left-hand
        column, and second player's strategy is listed on first row)
        :param legal_positions: all of the legal positions remaining
        :param samples: samples with strategies played, payoff values from monte carlo sampling, and game state
        """
        self.first_player, self.second_player = self.represent_players(player_order)
        self.legal_positions = legal_positions
        self.samples = samples
        self.y_axis_length = len(self.legal_positions)
        self.x_axis_length = self.y_axis_length - 1
        self.payoff_table = [[None] * C.TOTAL_STRATEGIES for sample in range(C.TOTAL_STRATEGIES)]

        const_string_length = 9
        padding = 2
        self.max_length = const_string_length + padding + len(str(C.SAMPLES))

    def pretty_print(self, item: str):
        """
        Pretty prints the item passed in so that the overall matrix looks pretty and is more easily readable
        :param item: item of string type
        """

        # if the item is empty or of None value, print empty spaces
        if not item:
            item = '|' + (self.max_length * ' ')
            print(item, end='')

        # otherwise, pad the item appropriately
        else:
            item_length = len(item)
            extra_spaces = self.max_length - item_length
            left_spaces = extra_spaces // 2
            right_spaces = extra_spaces - left_spaces
            pretty_item = '|' + (left_spaces * ' ') + item + (right_spaces * ' ')
            print(pretty_item, end='')

    def print_border_line(self):
        """
        Prints a border line
        """
        print('\n' + (((self.max_length + 1) * C.TOTAL_STRATEGIES) * '-'))

    def display_table(self):
        """
        Displays the entire Payoff Table in a human-readable format
        """
        strategies = np.arange(0, C.TOTAL_STRATEGIES, dtype=int)

        self.print_border_line()
        for strategy in strategies:
            self.pretty_print(str(strategy))

        for payoff in self.payoff_table:
            self.print_border_line()
            for p in payoff:
                self.pretty_print(str(p))
        self.print_border_line()

    def create_human_readable_table(self):
        """
        Creates the entire Payoff Table in a human-readable format
        """

        for payoff in self.samples:
            for p in payoff:
                p1, p2 = p.get_strategy()
                self.payoff_table[p1][p2] = p.get_payoff()

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

