import os
import zipfile
import pickle
import torch

def find_q_tables_dir():
    current_directory = os.getcwd()
    current_directory = current_directory.split("Connect4-Python")[0]
    connect_four_dir = os.path.join(current_directory, "Connect4-Python")
    return os.path.join(connect_four_dir, "q_tables_for_rl_agents")


def create_qtable_filename(winning_streak, board_shape, ql_index, depth):
    # return f"qlearning_player_ws_{winning_streak}_players_2_shape_{board_shape}_index_{ql_index}_depth_{depth}.pkl"
    return f"qlearning_player_ws_{winning_streak}_players_2_shape_{board_shape}_index_{ql_index}.pkl"


def get_rl_agent_save_path(winning_streak, board_shape, ql_index, depth):
    file_name = create_qtable_filename(winning_streak, board_shape, ql_index, depth)
    return os.path.join(find_q_tables_dir(), file_name)


def extract_files_from_zip(winning_streak, board_shape, index, depth):
    full_path_filename = get_rl_agent_save_path(winning_streak, board_shape, index, depth)
    if os.path.isfile(full_path_filename):
        return
    target_filename = create_qtable_filename(winning_streak, board_shape, index, depth)
    zip_filename = full_path_filename + ".zip"
    zip_directory = os.path.dirname(os.path.abspath(zip_filename))
    target_path = os.path.join(zip_directory, target_filename)
    with zipfile.ZipFile(zip_filename, 'r') as zip_file:
        for file_info in zip_file.infolist():
            if os.path.basename(file_info.filename) == target_filename:
                with zip_file.open(file_info.filename) as source_file:
                    with open(target_path, 'wb') as target_file:
                        target_file.write(source_file.read())

def get_qtable_from_file(full_path_filename):
    with open(full_path_filename, 'rb') as file_object:
        return pickle.load(file_object)

def save_rl_agent_qtable(file_name, rl_agent):
    with open(file_name, 'wb') as file_object:
        pickle.dump(rl_agent.q_table, file_object)

def zip_rl_agent_qtable(file_name):
    zip_filename = file_name + ".zip"
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        zip_file.write(file_name, compress_type=zipfile.ZIP_DEFLATED)


def board_to_one_hot_board(board, game_board_shape, num_of_players):
    rows, cols = game_board_shape[0], game_board_shape[1]
    one_hot_board = torch.zeros((num_of_players, rows, cols))
    for i in range(num_of_players):
        one_hot_board[i, ...] = (board == i).to(torch.int8)
    return one_hot_board

def pre_process_board(game_board, game_board_shape, num_of_players):
    """
    the parameter game_board can be tuple or np.array
    """
    rows, cols = game_board_shape[0], game_board_shape[1]
    board = torch.tensor(game_board).reshape((rows, cols))
    return board_to_one_hot_board(board, game_board_shape, num_of_players)
