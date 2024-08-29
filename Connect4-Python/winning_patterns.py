import numpy as np


class WinningPatterns:
    CONV_RES_SHAPES = {}
    INDICES_BY_X_Y_Z = {}
    # PATTERNS = {}

    @staticmethod
    def build_shapes(winning_streak, board_shape):
        is_3d = (len(board_shape) == 3 and board_shape[2] > 1)
        WinningPatterns.CONV_RES_SHAPES = {}

        temp_dict = {
            (1, 0, 0): (board_shape[0] - winning_streak + 1, board_shape[1], board_shape[2]),
            (0, 1, 0): (board_shape[0], board_shape[1] - winning_streak + 1, board_shape[2]),
            (0, 0, 1): (board_shape[0], board_shape[1], board_shape[2] - winning_streak + 1),
            (1, 1, 0): (board_shape[0] - winning_streak + 1, board_shape[1] - winning_streak + 1, board_shape[2]),
            (1, 0, 1): (board_shape[0] - winning_streak + 1, board_shape[1], board_shape[2] - winning_streak + 1),
            (0, 1, 1): (board_shape[0], board_shape[1] - winning_streak + 1, board_shape[2] - winning_streak + 1),
            (-1, 1, 0): (board_shape[0] - winning_streak + 1, board_shape[1] - winning_streak + 1, board_shape[2]),
            (-1, 0, 1): (board_shape[0] - winning_streak + 1, board_shape[1], board_shape[2] - winning_streak + 1),
            (0, -1, 1): (board_shape[0], board_shape[1] - winning_streak + 1, board_shape[2] - winning_streak + 1),
            (1, 1, 1): (board_shape[0] - winning_streak + 1, board_shape[1] - winning_streak + 1, board_shape[2] - winning_streak + 1),
            (1, -1, -1): (board_shape[0] - winning_streak + 1, board_shape[1] - winning_streak + 1, board_shape[2] - winning_streak + 1),
            (-1, 1, -1): (board_shape[0] - winning_streak + 1, board_shape[1] - winning_streak + 1, board_shape[2] - winning_streak + 1),
            (-1, -1, 1): (board_shape[0] - winning_streak + 1, board_shape[1] - winning_streak + 1, board_shape[2] - winning_streak + 1)
        }

        for direction, res_shape in temp_dict.items():
            if is_3d or direction[2] == 0:
                WinningPatterns.CONV_RES_SHAPES[direction] = temp_dict[direction]


        # # XYZ diagonal kernel
        # xyz_kernel = np.zeros((winning_streak, winning_streak, winning_streak))
        # for i in range(winning_streak):
        #     xyz_kernel[i, i, i] = 1
        #
        # # Anti-XYZ diagonal kernel 1 (reverse along z-axis)
        # anti_xyz_kernel_1 = np.zeros((winning_streak, winning_streak, winning_streak))
        # for i in range(winning_streak):
        #     anti_xyz_kernel_1[i, i, winning_streak - 1 - i] = 1
        #
        # # Anti-XYZ diagonal kernel 2 (reverse along y-axis)
        # anti_xyz_kernel_2 = np.zeros((winning_streak, winning_streak, winning_streak))
        # for i in range(winning_streak):
        #     anti_xyz_kernel_2[i, winning_streak - 1 - i, i] = 1
        #
        # # Anti-XYZ diagonal kernel 3 (reverse along x-axis)
        # anti_xyz_kernel_3 = np.zeros((winning_streak, winning_streak, winning_streak))
        # for i in range(winning_streak):
        #     anti_xyz_kernel_3[winning_streak - 1 - i, i, i] = 1
        #
        # WinningPatterns.PATTERNS = {
        #     (1, 0, 0): np.ones((winning_streak, 1, 1)),  # x-direction
        #     (0, 1, 0): np.ones((1, winning_streak, 1)),  # y-direction
        #     (0, 0, 1): np.ones((1, 1, winning_streak)),  # z-direction
        #     (1, 1, 0): np.eye(winning_streak).reshape((winning_streak, winning_streak, 1)),  # xy diagonal
        #     (1, 0, 1): np.eye(winning_streak).reshape((winning_streak, 1, winning_streak)),  # xz diagonal
        #     (0, 1, 1): np.eye(winning_streak).reshape((1, winning_streak, winning_streak)),  # yz diagonal
        #     (-1, 1, 0): np.fliplr(np.eye(winning_streak)).reshape((winning_streak, winning_streak, 1)),  # anti-xy diagonal
        #     (-1, 0, 1): np.fliplr(np.eye(winning_streak)).reshape((winning_streak, 1, winning_streak)),  # anti-xz diagonal
        #     (0, -1, 1): np.fliplr(np.eye(winning_streak)).reshape((1, winning_streak, winning_streak)),  # anti-yz diagonal
        #     (1, 1, 1): xyz_kernel,  # xyz diagonal
        #     (-1, -1, 1): anti_xyz_kernel_1,  # anti-xyz diagonal 1
        #     (-1, 1, -1): anti_xyz_kernel_2,  # anti-xyz diagonal 2
        #     (1, -1, -1): anti_xyz_kernel_3  # anti-xyz diagonal 3
        # }

    @staticmethod
    def build_needed_indices(winning_streak, last_disc_location):
        x, y, z = last_disc_location

        if last_disc_location in WinningPatterns.INDICES_BY_X_Y_Z:
            return WinningPatterns.INDICES_BY_X_Y_Z[last_disc_location]

        coordinates_dict_by_direction = {}
        x_cords = {
            1: WinningPatterns.build_range(1, x, winning_streak),
            0: np.array([x] * winning_streak),
            -1: WinningPatterns.build_range(-1, x, winning_streak)
        }

        y_cords = {
            1: WinningPatterns.build_range(1, y, winning_streak),
            0: np.array([y] * winning_streak),
            -1: WinningPatterns.build_range(-1, y, winning_streak)
        }

        z_cords = {
            1: WinningPatterns.build_range(1, z, winning_streak),
            0: np.array([z] * winning_streak),
            -1: WinningPatterns.build_range(-1, z, winning_streak)
        }

        for direction, res_shape in WinningPatterns.CONV_RES_SHAPES.items():
            dx, dy, dz = direction

            cur_x_cords = x_cords[dx]
            cur_y_cords = y_cords[dy]
            cur_z_cords = z_cords[dz]

            # cur_x_cords = WinningPatterns.build_range(dx, x, winning_streak)
            # cur_y_cords = WinningPatterns.build_range(dy, y, winning_streak)
            # cur_z_cords = WinningPatterns.build_range(dz, z, winning_streak)

            coordinates = np.vstack((cur_x_cords, cur_y_cords, cur_z_cords))
            valid_mask = (coordinates[0, :] >= 0) & (coordinates[0, :] < WinningPatterns.CONV_RES_SHAPES[direction][0]) & \
                         (coordinates[1, :] >= 0) & (coordinates[1, :] < WinningPatterns.CONV_RES_SHAPES[direction][1]) & \
                         (coordinates[2, :] >= 0) & (coordinates[2, :] < WinningPatterns.CONV_RES_SHAPES[direction][2])

            coordinates_dict_by_direction[direction] = coordinates[:, valid_mask]

        WinningPatterns.INDICES_BY_X_Y_Z[last_disc_location] = coordinates_dict_by_direction
        return coordinates_dict_by_direction

    @staticmethod
    def build_range(dim_delta, dim_val, winning_streak):
        cords = None
        if dim_delta == 1:
            cords = np.arange(dim_val - winning_streak + 1, dim_val + 1)
        elif dim_delta == 0:
            cords = np.array([dim_val] * winning_streak)
        elif dim_delta == -1:
            cords = np.arange(dim_val, dim_val - winning_streak, -1)

        return cords


