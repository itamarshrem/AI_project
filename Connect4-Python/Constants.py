import numpy as np

class Constants:

    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)

    PLAYER_COLORS = [RED, YELLOW, MAGENTA]
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    SQUARESIZE = 100

    WINNING_STREAK = 4
    KERNELS = []

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE

    size = (width, height)

    RADIUS = int(SQUARESIZE / 2 - 5)

    @staticmethod
    def set_winning_streak(winning_streak):
        Constants.WINNING_STREAK = winning_streak
        Constants.build_kernels()

    @staticmethod
    def build_kernels():
        winning_streak = Constants.WINNING_STREAK
        # XYZ diagonal kernel
        xyz_kernel = np.zeros((winning_streak, winning_streak, winning_streak))
        for i in range(winning_streak):
            xyz_kernel[i, i, i] = 1

        # Anti-XYZ diagonal kernel 1 (reverse along z-axis)
        anti_xyz_kernel_1 = np.zeros((winning_streak, winning_streak, winning_streak))
        for i in range(winning_streak):
            anti_xyz_kernel_1[i, i, winning_streak - 1 - i] = 1

        # Anti-XYZ diagonal kernel 2 (reverse along y-axis)
        anti_xyz_kernel_2 = np.zeros((winning_streak, winning_streak, winning_streak))
        for i in range(winning_streak):
            anti_xyz_kernel_2[i, winning_streak - 1 - i, i] = 1

        # Anti-XYZ diagonal kernel 3 (reverse along x-axis)
        anti_xyz_kernel_3 = np.zeros((winning_streak, winning_streak, winning_streak))
        for i in range(winning_streak):
            anti_xyz_kernel_3[winning_streak - 1 - i, i, i] = 1

        Constants.KERNELS = [
                np.ones((winning_streak, 1, 1)),  # x-direction
                np.ones((1, winning_streak, 1)),  # y-direction
                np.ones((1, 1, winning_streak)),  # z-direction
                np.eye(winning_streak).reshape((winning_streak, winning_streak, 1)),  # xy diagonal
                np.eye(winning_streak).reshape((winning_streak, 1, winning_streak)),  # xz diagonal
                np.eye(winning_streak).reshape((1, winning_streak, winning_streak)),  # yz diagonal
                np.fliplr(np.eye(winning_streak)).reshape((winning_streak, winning_streak, 1)),  # anti-xy diagonal
                np.fliplr(np.eye(winning_streak)).reshape((winning_streak, 1, winning_streak)),  # anti-xz diagonal
                np.fliplr(np.eye(winning_streak)).reshape((1, winning_streak, winning_streak)),  # anti-yz diagonal
                xyz_kernel,  # xyz diagonal
                anti_xyz_kernel_1,  # anti-xyz diagonal 1
                anti_xyz_kernel_2,  # anti-xyz diagonal 2
                anti_xyz_kernel_3  # anti-xyz diagonal 3
        ]
