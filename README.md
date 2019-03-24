# tic_tac_toe
A tic-tac-toe board of randomly chosen moves is generated up to a set number of moves (MOVES constant in constant.py).

Monte Carlo sampling is applied to the initial game state to predict expected values for random states. From the resulting samplings, a payoff table is created for the next two moves (aka strategies) by both players. Game theory analysis is applied to discover dominant strategies for both players.

After the payoff table is displayed, the game is played to completion using random move generation and the actual strategy is juxtaposed with the payoff values for the strategies that were implemented.

# instructions
* Clone or fork the repo.
* Run ```pip install -r requirements.txt``` to get the required dependencies.
* Go into **venv** and run ```game.py``` with your IDE or with python3 onward (this program was created with Python 3.7).

# modifications
* Adjust the number of samplings by going into ```constant.py``` and changing the ```SAMPLES``` constant. 
* Adjust the starting board state's number of moves by changing the ```MOVES``` constant in ```constant.py```.
* Have the start state randomly generated with the ```RANDOM``` state set to True, or set it statically by setting the ```STATIC``` constant to True. The other state should be False, but if both are set to True, the board will default to being randomly generated.
