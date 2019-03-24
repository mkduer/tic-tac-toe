# tic_tac_toe
A tic-tac-toe board of randomly chosen moves is generated up to a set number of moves (MOVES constant in constant.py).

Monte Carlo sampling is applied to the initial game state to predict expected values for random states. From the resulting samplings, a payoff table is created for the next two moves (aka strategies) by both players. Game theory analysis is applied to discover dominant strategies for both players.

After the payoff table is displayed, the game is played to completion using random move generation and the actual strategy is juxtaposed with the payoff values for the strategies that were implemented.
