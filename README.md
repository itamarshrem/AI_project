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
- `--eval_functions` (`-ef`): Specifies the evaluation function for each player. Choices include `"simple"`, `"complex"`, `"defensive"`, `"offensive"`, `"ibef2"`, `"none"`, and `"only_best_opponent"`. (These are relevant and needed for `minmax`, `alpha_beta`, and `baseline` players only, the default value is `"none"` for all players).
- `--depths` (`-d`): Search depth for each player. This is relevant for `minmax` and `alpha_beta` players only, and it has a default value of 2 * number of players for relevant players.
- `--gamma` (`-g`): Probability of a random action for search agents. This is relevant for `minmax` and `alpha_beta` players only (Gamma=0 is deterministic and it is the default value).
- `--winning_streak` (`--winning_streak`): Number of consecutive pieces required to win the game (required).
- `--num_of_games` (`-ng`): Number of consecutive games to be played (required).
- `--display_screen` (`-ui`): Enables the game UI (optional).
- `--load_rl_agent` (`-lrl`): Loads a previously saved RL agent (relevant only when using the `rl_agent` player).
- `--rl_currently_learning`: Enables the RL agent's learning mode (relevant only when using the `rl_agent` player).


### Note on Argument Generalization

In order to allow generalization across different player types, all of the following arguments are **required** when running the game:
- `--board_shape`
- `--players`
- `--winning_streak`
- `--num_of_games`
  
Additional **important note** is that for these arguments:
- `--eval_functions`
- `--depths`
- `--gamma`
  
when inputed or modified, they must be inputed for all players, even if they are not relevant for some of them (players that do not use them will ignore these values).



## Example Commands
**Complex Agent(Depth = 3) vs Offensive Agent vs Random Agent**

Run 100 games between an Alpha-Beta with the complex heuristic, a baseline player using the offensive evaluation function, and a random player.
   
   ```bash
   python Connect4-Python/connect4.py -size 6 7 1 -p alpha_beta baseline random -ef complex offensive none --depths 3 0 0  --winning_streak 4 --num_of_games 100
   ```

**Complex Agent(Depth = 4) vs Offensive Agent**

Run 100 games between an Alpha-Beta with the complex heuristic and a baseline player using the offensive evaluation function.
   
   ```bash
   python Connect4-Python/connect4.py --board_shape 6 7 1 --players alpha_beta baseline --eval_functions complex offensive  --depths 4 1 --winning_streak 4 --num_of_games 100
   ```

**Human vs Complex Agent (Depth = 6)**

Run a single game between a human player and an Alpha-Beta agent using a complex evaluation function, in depth 2.

   ```bash
   python Connect4-Python/connect4.py --board_shape 6 7 1 --players human alpha_beta --eval_functions none complex --depths 1 4 --winning_streak 4 --num_of_games 1 -ui
   ```


**RL Agent vs Complex Agent(Depth = 2, Gamma = 0.2)**

Test the RL agent trained earlier against a Complex Agent with depth 2 and probability of 0.2 to make a random move.

   ```bash
   python Connect4-Python/connect4.py --board_shape 6 7 1 --players rl_agent alpha_beta --eval_functions none complex --depths 1 2 --gamma 0 0.2 --winning_streak 4 --num_of_games 1000 --load_rl_agent
   ```

**RL Agent vs Human**

Test the RL agent trained earlier against human. notice that the Rl agent we provided you was trained as the first player.
If you want to test it as the second player you need to train it again as the second player.

   ```bash
   python Connect4-Python/connect4.py --board_shape 6 7 1 --players rl_agent human --eval_functions none none  --winning_streak 4 --num_of_games 1 -ui --load_rl_agent
   ```

### 3D Board (Console Interface)
The game also supports 3D board configurations for Connect 4, where the board has multiple depths. When using a 3D board:
- The board is displayed in the console, with each depth represented as a separate grid.
- The player inputs their move by specifying both the column and depth.

### Example:

For running with a 3D board configuration (console-based):
   ```bash
   python Connect4-Python/connect4.py --board_shape 6 7 5 --players baseline human --eval_functions defensive none --winning_streak 4 --num_of_games 1 -ui
   ```





