from sample import Sample
import numpy as np
import constant as C
from math import nan

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
        self.cell_length = const_string_length + padding + len(str(C.SAMPLES))
        self.max_length = (self.cell_length + 1) * (C.TOTAL_STRATEGIES + 1)

    def pretty_print(self, item: str):
        """
        Pretty prints the item passed in so that the overall matrix looks pretty and is more easily readable
        :param item: item of string type
        """

        # if the item is empty or of None value, print empty spaces
        if not item:
            item = '|' + (self.cell_length * ' ')
            print(item, end='')

        # otherwise, pad the item appropriately
        else:
            item_length = len(item)
            extra_spaces = self.cell_length - item_length
            left_spaces = extra_spaces // 2
            right_spaces = extra_spaces - left_spaces
            pretty_item = '|' + (left_spaces * ' ') + item + (right_spaces * ' ')
            print(pretty_item, end='')

    def print_header(self):
        """
        Prints payoff table title
        """

        # Print Title
        title = '(pl: rows, p2: cols)     PAYOFF TABLE     (' + str(self.first_player) + '\'s wins, ' + \
                str(self.second_player) + '\'s wins, stalemates)'
        #title = 'PAYOFF TABLE     (Player 1\'s wins, Player 2\'s wins, Stalemates)'
        title_len = len(title)
        extra_spaces = self.max_length - title_len
        left_spaces = extra_spaces // 2
        right_spaces = extra_spaces - left_spaces
        title_details = (left_spaces * ' ') + title + (right_spaces * ' ')
        print(title_details, end='')

    def print_border_line(self, breakline: bool=True):
        """
        Prints a border line
        :param breakline: adds a newline if True, no newline if False
        """
        if breakline:
            print('\n' + (self.max_length * '-'))
        else:
            print((self.max_length * '-'))

    def display_table(self):
        """
        Displays the entire Payoff Table in a human-readable format
        """

        self.print_header()

        for payoff in self.payoff_table:
            self.print_border_line()
            for p in payoff:
                self.pretty_print(str(p))
        self.print_border_line()

    def create_human_readable_table(self):
        """
        Creates the entire Payoff Table in a human-readable format
        """
        strategies = list(np.arange(0, C.TOTAL_STRATEGIES, dtype=int))

        # build payoff table from strategies
        for payoff in self.samples:
            for p in payoff:
                p1, p2 = p.get_strategy()

                # Catch condition if p2 is a floating nan
                # This means that p1 already won the game and p2 has no strategies
                if type(p2) == int:
                    self.payoff_table[p1][p2] = str(p.get_payoff())
                else:
                    for moves in self.legal_positions:
                        if moves != p1:
                            self.payoff_table[p1][moves] = str(p.get_payoff())

        # add player 1's strategies
        for strategy, payoff in zip(strategies, self.payoff_table):
            payoff.insert(0, strategy)

        # prepend player 2's strategies
        strategies.insert(0, 'Strategies')
        self.payoff_table.insert(0, strategies)

    def represent_players(self, player_order) -> str:
        """
        Returns the pieces that represent each player
        :param player_order: the first and second player's values
        :return the first player's pice, the second player's piece (e.g. X, O)
        """
        players = ['', '']

        for i in range(len(player_order)):
            if player_order[i] == 0:
                players[i] = 'X'
            elif player_order[i] == 1:
                players[i] = 'O'

        return players[0], players[1]
