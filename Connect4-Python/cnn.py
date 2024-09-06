import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
import utils
import matplotlib.pyplot as plt

EMPTY_CELL = -1

LR = 0.01
BATCH_SIZE = 100
EPOCHS = 20

device = ("cuda" if torch.cuda.is_available() else "cpu")


def train_model(dataloader, model, loss_fn, optimizer, loss_arr_train):
    num_batches = len(dataloader)
    model.train()
    train_loss = 0
    for x, y_true in dataloader:
        x, y_true = x.to(device), y_true.to(device)
        y = model(x)
        params = torch.cat([x.view(-1) for x in model.parameters()])
        regularization_loss = torch.norm(params, 1) / len(list(model.parameters()))
        alpha = 0.01
        loss = loss_fn(y, y_true) + alpha * regularization_loss
        print(f"loss: {loss.item()}, regularization_loss: {regularization_loss.item()}")
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
    train_loss /= num_batches
    loss_arr_train.append(train_loss)
    print(f'Train set: Average loss: {train_loss:>8f}')


def test_model(dataloader, model, loss_fn, loss_arr_test):
    num_batches = len(dataloader)
    model.eval()
    test_loss = 0
    with torch.no_grad():
        for x, y_true in dataloader:
            x, y_true = x.to(device), y_true.to(device)
            y = model(x)
            params = torch.cat([x.view(-1) for x in model.parameters()])
            regularization_loss = torch.norm(params, 1) / len(list(model.parameters()))
            alpha = 0.01
            loss = loss_fn(y, y_true) + alpha * regularization_loss
            test_loss += loss.item()
    test_loss /= num_batches
    loss_arr_test.append(test_loss)


def create_data_set(path_to_q_table, num_of_players, board_shape, player_index):
    # the qtable dataset contains 732597 keys
    #the board_grades contains 697848 entries
    # create a data set for the model from the q_table
    q_table = utils.get_qtable_from_file(path_to_q_table)
    board_grades = {}
    for state, action_values in q_table.items():
        board = np.array(state).reshape(*board_shape)
        board = board[:, :, 0]  # works only on 2D boards
        action_values = action_values[:, 0]
        for col, value in enumerate(action_values):
            if value == 0:
                continue
            if abs(value) > 500:  # we want to truncate huge values so the cnn model won't try to adapt to outliers
                value = np.sign(value) * 500
            board = place_disc(board, col, player_index)
            board_key = tuple(board.flatten())
            if board_key not in board_grades:
                board_grades[board_key] = []
            board_grades[board_key].append(value)
    data = torch.zeros(len(board_grades), num_of_players, board_shape[0], board_shape[1])
    labels = torch.zeros(len(board_grades))
    for i, (key_board, grades) in enumerate(board_grades.items()):
        board = utils.pre_process_board(key_board, board_shape, num_of_players, device)
        value = sum(grades) / len(grades)
        data[i, ...] = board
        labels[i] = value
    dataset = TensorDataset(data, labels)
    return dataset


def place_disc(board, col, player_index):
    board = board.copy()
    row = np.argmax(board[:, col] == EMPTY_CELL)
    board[row, col] = player_index
    return board


class CNN(nn.Module):
    def __init__(self, one_hot_board_shape, winning_streak):
        super(CNN, self).__init__()
        self.num_of_players, self.rows, self.cols = one_hot_board_shape
        assert self.cols > (winning_streak - 1) and (self.rows > winning_streak - 1)
        self.winning_streak = winning_streak
        num_of_directions = 4
        self.out_channels = self.num_of_players * self.winning_streak * num_of_directions
        self.conv1 = nn.Conv2d(self.num_of_players, self.out_channels, winning_streak, stride=1)  # 6 X 7 -> 3 X 4
        self.conv2 = nn.Conv2d(self.out_channels, self.out_channels, 3, stride=1, padding=1)  # 3 X 4 -> 3 X 4
        # self.cols - winning_streak + 1
        self.out_flatten_length = (self.rows - winning_streak + 1) * (self.cols - winning_streak + 1) * self.out_channels
        self.fc1 = nn.Linear(self.out_flatten_length, self.out_flatten_length)
        self.fc2 = nn.Linear(self.out_flatten_length, self.cols)
        # self.fc2 = nn.Linear(self.out_flatten_length, 1)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(-1, self.out_flatten_length)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        x = torch.softmax(x, dim=1)
        x = x.view(-1, self.cols, 1)
        return x

    def predict(self, x):
        return self.forward(x).detach().numpy()


def plot_loss(train_loss_arr, test_loss_arr, loss_str):
    fig, ax = plt.subplots()

    # Plot loss_arr_train
    ax.plot(train_loss_arr, label='Train Loss', marker='o', linestyle='-', color='b')

    # Plot loss_arr_test
    ax.plot(test_loss_arr, label='Test Loss', marker='x', linestyle='--', color='r')

    # Add labels and title
    ax.set_xlabel('Epoch')
    ax.set_ylabel(loss_str)
    ax.set_title('Train vs. Test Loss')

    # Add legend
    ax.legend()
    plt.savefig('Train vs Test Loss.png')
    # Show the plot
    plt.show()


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    default_players_num = 2
    parser.add_argument('-size', '--board_shape', type=int, nargs=3, default=[6, 7, 1], help='size of the board')
    parser.add_argument('-d', '--depths', type=int, nargs="*", default=[2] * default_players_num, help='Depth of the search tree')
    parser.add_argument('-ws', '--winning_streak', type=int, default=4, help='Number of consecutive pieces to win')
    parser.add_argument('-ng', '--num_of_games', type=int, default=1, help='Number of consecutive games')

    return parser.parse_args()


def train_and_test(train, test, cnn_model):
    train_loader = DataLoader(train, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test, batch_size=BATCH_SIZE, shuffle=True)
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.Adam(cnn_model.parameters(), lr=LR)

    loss_arr_train = []
    loss_arr_test = []
    for epoch in range(EPOCHS):
        print(f'Epoch {epoch + 1}\n-------------------------------')
        train_model(train_loader, cnn_model, loss_fn, optimizer, loss_arr_train)
        test_model(test_loader, cnn_model, loss_fn, loss_arr_test)
        torch.save(cnn_model.state_dict(), 'Connect4-Python/cnn/cnn_model_weights.pth')
    plot_loss(loss_arr_train, loss_arr_test, "MSE loss")
    print('Done!')
    print('Model saved!')


def main():
    # args = parse_args()

    train_from_zero = True
    should_create_dataset = True

    print("Running on:", device)
    full_path_filename = utils.get_rl_agent_save_path(4, [6, 7, 1], 0)
    cnn_model = CNN((2, 6, 7), 4).to(device)

    if not train_from_zero:
        cnn_model.load_state_dict(torch.load('Connect4-Python/cnn/cnn_model_weights.pth'))

    if should_create_dataset:
        dataset = create_data_set(full_path_filename, 2, (6, 7, 1), 0)
        torch.save(dataset, 'Connect4-Python/cnn/cnn_dataset.pt')

    dataset = torch.load('Connect4-Python/cnn/cnn_dataset.pt')
    train, test = torch.utils.data.random_split(dataset,[int(0.8 * len(dataset)), len(dataset) - int(0.8 * len(dataset))])
    train_and_test(train, test, cnn_model)

if __name__ == '__main__':
    main()
