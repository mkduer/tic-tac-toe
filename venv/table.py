from sample import Sample

class Table:

    def display_payoff_table(self, player_order: [int], legal_positions: [int], payoff_table: [Sample]):
        """
        Displays the entire Payoff Table in a human-readable format
        :param player_order: which player goes first/second (first player's strategies are listed in left-hand
        column, and second player's strategy is listed on first row)
        :param legal_positions: all of the legal positions remaining
        :param payoff_table: payoff table with strategies played, payoff values from monte carlo sampling, and game state
        """
        y_axis_length = len(legal_positions)
        x_axis_length = y_axis_length - 1

        # TODO: Run a check to see if either player has no legal positions and print the relevant message

#        for player1_strategy in player1_legal_pos:

        # TEST values
        print(f'player order : {player_order}\n'
              f'legal positions: {legal_positions}\n')

        for payoff in payoff_table:
            print(payoff)
        for payoff in payoff_table:
            for p in payoff:
                #p.display_sample()  # TODO remove if not using
                p.display_payoff()

