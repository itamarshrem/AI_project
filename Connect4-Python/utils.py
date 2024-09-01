import os
import zipfile
import pickle

def find_q_tables_dir():
    current_directory = os.getcwd()
    current_directory = current_directory.split("Connect4-Python")[0]
    connect_four_dir = os.path.join(current_directory, "Connect4-Python")
    return os.path.join(connect_four_dir, "q_tables_for_rl_agents")


def create_qtable_filename(winning_streak, board_shape, ql_index, depth):
    return f"qlearning_player_ws_{winning_streak}_players_2_shape_{board_shape}_index_{ql_index}_depth_{depth}.pkl"


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