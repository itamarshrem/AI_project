import numpy as np
import torch
from torch import nn
from board import Board
from torch.utils.data import DataLoader, TensorDataset
import utils

class CnnAgent:
    # by getting a board the agent will run a cnn model to get the value of the model and than return the best action

    def __init__(self, model, player_index, winning_streak, board_shape):
        self.model = model
        self.player_index = player_index
        self.winning_streak = winning_streak
        self.board_shape = board_shape

    def get_action(self, board, num_of_players, winning_streak, ui):
        # get the value of the board
        value = self._get_board_value(board)
        # get the best action
        action = self._get_best_action(board, value)
        return action

    def _get_board_value(self, board):
        # get the value of the board
        return self.model.predict(board.board.reshape(1, *self.board_shape))[0]

    def _get_best_action(self, board):
        # get the best action
        legal_actions = board.get_legal_actions(self.winning_streak)
        best_action = None
        best_value = -float('inf')
        for action in legal_actions:
            board_copy = board.__copy__()
            board_copy.apply_action(action, self.player_index, self.winning_streak)
            action_value = self._get_board_value(board_copy)
            if action_value > best_value:
                best_value = action_value
                best_action = action
        return best_action

    def train_model(self, dataloader, model, loss_fn, optimizer, loss_arr_train):
        num_batches = len(dataloader)
        model.train()
        train_loss = 0
        for x, y_true in dataloader:
            x, y_true = x.to(device), y_true.to(device)
            y = model(x)
            loss = loss_fn(y, y_true)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            train_loss += loss.item()
        train_loss /= num_batches
        loss_arr_train.append(train_loss)
        print(f'Train set: Average loss: {train_loss:>8f}')

    def test_model(self, dataloader, model, loss_fn, loss_arr_test):
        num_batches = len(dataloader)
        model.eval()
        test_loss = 0
        with torch.no_grad():
            for x, y_true in dataloader:
                x, y_true = x.to(device), y_true.to(device)
                y = model(x)
                loss = loss_fn(y, y_true)
                test_loss += loss.item()
        test_loss /= num_batches
        loss_arr_test.append(test_loss)

    def create_data_set(self, path_to_q_table, num_of_players):
        # create a data set for the model from the q_table
        with open(path_to_q_table, 'rb') as file:
            q_table = pickle.load(file)
        board_grades = {}
        for state, action_values in q_table.items():
            board = np.array(state).reshape(*self.board_shape)
            board = board[:, :, 0]  # works only on 2D boards
            action_values = action_values[:, 0]
            for col, value in enumerate(action_values):
                if value == 0:
                    pass
                board = self.place_disc(board, col, self.player_index)
                board_key = tuple(board.flatten())
                if board_key not in board_grades:
                    board_grades[board_key] = []
                board_grades[board_key].append(value)
        data = torch.tensor.zeros(len(board_grades), num_of_players, self.board_shape[0], self.board_shape[1])
        labels = torch.tensor.zeros(len(board_grades))
        for i, (key_board, grades) in enumerate(board_grades.items()):
            board = np.array(key_board).reshape(self.board_shape[0], self.board_shape[1])
            board = self.board_to_one_hot_board(board, num_of_players)
            value = sum(grades) / len(grades)
            data[i, ...] = board
            labels[i] = value
        dataset = TensorDataset(data, labels)
        return dataset

    def board_to_one_hot_board(self, board, num_of_players):
        one_hot_board = np.zeros((num_of_players, self.board_shape[0], self.board_shape[1]))
        for i in range(num_of_players):
            one_hot_board[i, ...] = (board == i).as_type(np.int8)

    def place_disc(self, board, col, player_index):
        board = board.copy()
        row = np.argmax(board[:, col] == Board.EMPTY_CELL)
        board[row, col] = player_index
        return board



LR = 0.01
BATCH_SIZE = 20
EPOCHS = 125
device = ("cuda" if torch.cuda.is_available() else "cpu")


class CNN(nn.Module):
    def __init__(self, board_shape, winning_streak, num_of_players):
        super(CNN, self).__init__()
        self.winning_streak = winning_streak
        self.conv1 = nn.Conv2d(num_of_players, 12, winning_streak, stride=1)  # 6 X 7 -> 3 X 4
        self.conv2 = nn.Conv2d(12, 12, 3, stride=1)  # 3 X 4 -> 1 X 2
        self.fc1 = nn.Linear((board_shape[0] - 2 * winning_streak) * (board_shape[1] - 2 * winning_streak) * 12, 50)
        self.fc2 = nn.Linear(50, 1)
        self.board_shape = board_shape

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(-1, (self.board_shape[0] - 2 * self.winning_streak) * (self.board_shape[1] - 2 * self.winning_streak) * 12)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def predict(self, x):
        return self.forward(torch.tensor(x, dtype=torch.float32)).detach().numpy()

if __name__ == '__main__':
