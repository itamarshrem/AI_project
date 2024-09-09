# Connect 4 AI Game
This repository contains a Connect 4 game with several AI players implemented, including Random, MinMax, Alpha-Beta, and RL agents. It allows users to configure various aspects of the game, such as the board size, players, evaluation functions, search tree depth, and game rules.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/itamarshrem/AI_project.git
   ```

2. Install the necessary Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Overview
The game supports the following types of players:

- **human**: Manual player.
- **random**: Random agent that selects moves randomly.
- **minmax**: Min-Max agent that searches for the best move using the Min-Max algorithm.
- **alpha_beta**: Alpha-Beta pruning agent to optimize Min-Max search.
- **rl_agent**: Reinforcement Learning agent (QLearning).
- **baseline**: Baseline agent that uses predefined evaluation strategies (offensive or defensive).

Each player can be configured with a different evaluation function, search depth, and other parameters.

## Command Line Arguments
- `--board_shape` (`-size`): Specifies the board size (required).
- `--players` (`-p`): List of players participating in the game (required). Choices include `"human"`, `"random"`, `"minmax"`, `"alpha_beta"`, `"rl_agent"`, and `"baseline"`.
- `--eval_functions` (`-ef`): Specifies the evaluation function for each player (required). Choices include `"simple"`, `"complex"`, `"defensive"`, `"offensive"`, `"ibef2"`, `"none"`, and `"only_best_opponent"`. These are relevant for `minmax`, `alpha_beta`, and `baseline` players only).
- `--depths` (`-d`): Search depth for each player (required). This is relevant for `minmax` and `alpha_beta` players only.
- `--gamma` (`-g`): Probability of a random action for search agents (required). This is relevant for `minmax` and `alpha_beta` players only (Gamma=0 is deterministic).
- `--winning_streak` (`-ws`): Number of consecutive pieces required to win the game (required).
- `--num_of_games` (`-ng`): Number of consecutive games to be played (required).
- `--display_screen` (`-ui`): Enables the game UI (optional).
- `--load_rl_agent` (`-lrl`): Loads a previously saved RL agent (relevant only when using the `rl_agent` player).
- `--rl_currently_learning`: Enables the RL agent's learning mode (relevant only when using the `rl_agent` player).
- `--board_configuration` (`-bc`): Starts a game with a specific board setup (optional). Choices include `"None"` and `"edge_case1"`.

### Note on Argument Generalization

In order to allow generalization across different player types, all of the following arguments are **required** when running the game:
- `--board_shape`
- `--players`
- `--eval_functions`
- `--depths`
- `--gamma`
- `--winning_streak`
- `--num_of_games`

However, not all arguments are relevant to every player. For example:
- **Random players** do not use `depth` or `gamma`, so these values are ignored for them.
- **RL agents** do not use `depth` or `gamma` unless specified for training purposes.

This setup allows flexibility while ensuring that all required arguments are provided for the relevant players.

## Example Commands
**Alpha-Beta vs Offensive Agent (Gamma = 0.6)**

Run 100 games between a baseline player and an Alpha-Beta agent using the offensive evaluation function.
   
   ```bash
   python connect4_game.py -size 6 7 5 -p baseline alpha_beta -ef offensive complex -d 1 4 -g 0 0.6 -ws 4 -ng 100
   ```

**Defensive vs Complex Agent (Depth = 2)**

Run 1000 games between a baseline player with a defensive evaluation function and an Alpha-Beta agent using a complex evaluation function.

   ```bash
   python connect4_game.py -size 6 7 1 -p baseline alpha_beta -ef defensive complex -d 1 2 -g 0 0 -ws 4 -ng 1000
   ```

**RL Training vs Alpha-Beta Agent (Gamma = 0.95)**

Train an RL agent against an Alpha-Beta agent for 100,000 games. The RL agent has gamma = 0 and the Alpha-Beta agent has gamma = 0.95.

   ```bash
   python connect4_game.py -size 6 7 1 -p rl_agent alpha_beta -ef none complex -d 2 2 -ws 4 -ng 100000 -g 0 0.95 --rl_currently_learning
   ```

**Testing RL Agent vs Defensive Agent**

Test the RL agent trained earlier against a baseline player with a defensive evaluation function for 1000 games.

   ```bash
   python connect4_game.py -size 6 7 1 -p rl_agent baseline -ef none defensive -d 1 1 -g 0 0 -ws 4 -ng 1000 -lrl
   ```

## Rl Agent Training
The RL agent can be trained by running the game with the `--rl_currently_learning` flag enabled. It allows the RL agent to update its Q-table as it plays games against other agents.

To load a saved RL agent, ensure that you have the `-lrl` flag enabled.

## Graphical User Interface (GUI)
This game includes a GUI for a more interactive player experience. The GUI is implemented using `pygame` and can be enabled using the `--display_screen` (or `-ui`) argument.

### Features of the GUI
- Displays the Connect 4 board with rows and columns.
- Each player's move is displayed with different colors (Red, Yellow, etc.).
- The player can interact with the game by selecting a column for their move using mouse clicks.
- The board updates dynamically after each move.
- The game result (win or tie) is shown on the screen at the end of the game.

### 3D Board (Console Interface)
The game also supports 3D board configurations for Connect 4, where the board has multiple depths. When using a 3D board:
- The board is displayed in the console, with each depth represented as a separate grid.
- The player inputs their move by specifying both the column and depth.

### Example Commands for Running the Game with GUI
To run a game with the GUI enabled:
   ```bash
   python connect4_game.py -size 6 7 1 -p baseline human -ef none simple -d 1 1 -ws 4 -ng 1 -ui
   ```

For running with a 3D board configuration (console-based):
   ```bash
   python connect4_game.py -size 6 7 5 -p baseline human -ef none simple -d 1 1 -ws 4 -ng 1 -ui
   ```

## Game Prints and Output Explanation

During the game, the console displays real-time information about each game, including performance metrics and game outcomes. Below is a detailed explanation of the key prints that appear:

### Game Execution Time
For each game, the time taken to complete the game is printed:
   
      ```
      game x: time taken: y seconds
      ```

This shows the game number (`x`) and the time (in seconds) it took for the game to run (`y seconds`).

### Player Wins and Winning Percentage
After each game, the winner is printed along with their index and their cumulative winning percentage:

      ```
      player PLayer_Details with index x won the game. winning percentage: y%
      ```

This shows the player's details (`Player_Details`), their index (`x`), and their cumulative winning percentage (`y%`).

### Final Summary After All Games
Once all games are complete, a summary of the results is printed:

      ```
      player PLayer_Details1 (index x1) won y1 games. winning percentage: z1% 
      player PLayer_Details2 (index x2) won y2 games. winning percentage: z2%
      ... ( for all players) 
      number of ties: a, tie percentage: b%
      ```

This shows the number of games won by each player, their winning percentage, the number of ties, and the tie percentage.

### Average Step Time for Each Player
After the game series concludes, the average step time for each player is printed:

      ```
      player PLayer_Details1 average step time: x1
      player PLayer_Details2 average step time: x2
      ```

This shows the average time taken by each player to make a move.




