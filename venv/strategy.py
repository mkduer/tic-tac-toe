import constant as C
from board import Board
from copy import deepcopy

class Strategy:

    def __init__(self, root: Board):
        self.root = root
        self.children = []
        self.payoff_table = []

    def analysis(self):
        """
        Runs all of the steps of analysis:
        - Finding root's children
        - Sampling with Monte Carlo
        - Generating a payoff table
        """
        self.children = self.find_children(self.root)
        self.monte_carlo_sampling()

    def find_children(self, node: Board) -> [Board]:
        """
        Finds all possible child states based on the parent state
        """
        return node.discover_children()

    def monte_carlo_sampling(self):
        """
        Sample from root and return strategy probabilities
        :return: sample state values
        """

        # TODO: initialize table to contain all of the samples (test if you can use a numpy matrix to hold the objects)

        for child, position in self.children:
            grandchildren = []
            print(f'CHILD after adding position {position}:')
            child.display()
            print(f'GRANDCHILDREN:')
            # for each grandchild (aka remaining legal moves in children)
            # generate new Board(grandchild) using grandchild
            # run SAMPLE number of times while collecting (O won, X won, stalemate)
            # save as a Sample with all of the data
            # save the Sample to the specific coordinate it belongs to in the payoff table  
            print(f'======== DONE ========')

        # TODO sample n (player 1) states by n - 1 (player 2) states
        # TODO: try using a generator


    def get_state(self) -> [int]:
        """
        :return: returns the board's current state
        """
        return self.state


    def create_payoff_table(self):
        """
        Samples from the starting board state to generate a (0, 1, -1, -2) probability out of a total constant sampling
        where the returned result reflects (Number of times O won, Number of times X won, Stalemates)
        off of the next two possible moves in the game.
        """

        # if there are no children
        if len(self.children) < 1:
            return (0, 0, 0)

        # sample each child and save the probabilities
        for child in self.children:
            payoff = self.monte_carlo_sampling(child)
            self.payoff_table.append(payoff)

    def display_payoff_table(self):
        """
        Displays payoff table
        """
        print(f'PAYOFF TABLE:\n{self.payoff_table}')
