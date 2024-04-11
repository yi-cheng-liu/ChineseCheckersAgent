from __future__ import print_function
import numpy as np
from config import *
import board_utils
import operator
from collections import deque


class Board:
    def __init__(self, randomised=False):
        """
        Get the numpy array representing this board.
        Array is shaped 7x7x3, where the first 7x7 plane
        is the current board, while the latter are the
        two previous steps.
        PLAYER_ONE and PLAYER_TWO's checkers are initialised
        at bottom left and top right corners respectively.
        """
        self.board = np.zeros((BOARD_WIDTH, BOARD_HEIGHT, BOARD_HIST_MOVES), dtype='uint8')  # Initialize empty board
        # self.board[:, :, 0] = np.array([[0, 0, 0, 0, 2, 2, 2],
        #                                 [0, 0, 0, 0, 0, 2, 2],
        #                                 [0, 0, 0, 0, 0, 0, 2],
        #                                 [0, 0, 0, 0, 0, 0, 0],
        #                                 [1, 0, 0, 0, 0, 0, 0],
        #                                 [1, 1, 0, 0, 0, 0, 0],
        #                                 [1, 1, 1, 0, 0, 0, 0]])
        
        self.board[:, :, 0] = np.array([[9, 9, 9, 9, 9,   9, 9, 9, 9, 9,   9, 9, 1, 9, 9,   9, 9],
                                        [9, 9, 9, 9, 9,   9, 9, 9, 9, 9,   9, 1, 1, 9, 9,   9, 9],
                                        [9, 9, 9, 9, 9,   9, 9, 9, 9, 9,   1, 1, 1, 9, 9,   9, 9],
                                        [9, 9, 9, 9, 9,   9, 9, 9, 9, 1,   1, 1, 1, 9, 9,   9, 9],
                                        [9, 9, 9, 9, 2,   2, 2, 2, 0, 0,   0, 0, 0, 6, 6,   6, 6],

                                        [9, 9, 9, 9, 2,   2, 2, 0, 0, 0,   0, 0, 0, 6, 6,   6, 9],
                                        [9, 9, 9, 9, 2,   2, 0, 0, 0, 0,   0, 0, 0, 6, 6,   9, 9],
                                        [9, 9, 9, 9, 2,   0, 0, 0, 0, 0,   0, 0, 0, 6, 9,   9, 9],
                                        [9, 9, 9, 9, 0,   0, 0, 0, 0, 0,   0, 0, 0, 9, 9,   9, 9],
                                        [9, 9, 9, 3, 0,   0, 0, 0, 0, 0,   0, 0, 5, 9, 9,   9, 9],

                                        [9, 9, 3, 3, 0,   0, 0, 0, 0, 0,   0, 5, 5, 9, 9,   9, 9],
                                        [9, 3, 3, 3, 0,   0, 0, 0, 0, 0,   5, 5, 5, 9, 9,   9, 9],
                                        [3, 3, 3, 3, 0,   0, 0, 0, 0, 5,   5, 5, 5, 9, 9,   9, 9],
                                        [9, 9, 9, 9, 4,   4, 4, 4, 9, 9,   9, 9, 9, 9, 9,   9, 9],
                                        [9, 9, 9, 9, 4,   4, 4, 9, 9, 9,   9, 9, 9, 9, 9,   9, 9],

                                        [9, 9, 9, 9, 4,   4, 9, 9, 9, 9,   9, 9, 9, 9, 9,   9, 9],
                                        [9, 9, 9, 9, 4,   9, 9, 9, 9, 9,   9, 9, 9, 9, 9,   9, 9]])

        # == Directions Map ==
        #
        #   NW north
        #  west     east
        #      south SE
        self.directions = [
            (-1, 0),    # north
            (0, 1),     # east
            (1, 1),     # southeast
            (1, 0),     # south
            (0, -1),    # west
            (-1, -1)    # northwest
        ]

        # self.checkers_pos = [None,
        #                      {0: (BOARD_HEIGHT-1, 0), 1: (BOARD_HEIGHT-2, 0), 2: (BOARD_HEIGHT-1, 1),
        #                       3: (BOARD_HEIGHT-3, 0), 4: (BOARD_HEIGHT-2, 1), 5: (BOARD_HEIGHT-1, 2)},
        #                      {0: (0, BOARD_WIDTH-1), 1: (1, BOARD_WIDTH-1), 2: (0, BOARD_WIDTH-2),
        #                       3: (2, BOARD_WIDTH-1), 4: (1, BOARD_WIDTH-2), 5: (0, BOARD_WIDTH-3)}]

        # self.checkers_id = [None,
        #                     {(BOARD_HEIGHT-1, 0): 0, (BOARD_HEIGHT-2, 0): 1, (BOARD_HEIGHT-1, 1): 2,
        #                      (BOARD_HEIGHT-3, 0): 3, (BOARD_HEIGHT-2, 1): 4, (BOARD_HEIGHT-1, 2): 5},
        #                     {(0, BOARD_WIDTH-1): 0, (1, BOARD_WIDTH-1): 1, (0, BOARD_WIDTH-2): 2,
        #                      (2, BOARD_WIDTH-1): 3, (1, BOARD_WIDTH-2): 4, (0, BOARD_WIDTH-3): 5}]
        
        self.checkers_pos = [None,
                     {0: (0, 12), 1: (1, 11), 2: (1, 12), 3: (2, 10), 4: (2, 11), 5: (2, 12),
                      6: (3, 9), 7: (3, 10), 8: (3, 11), 9: (3, 12)},
                     {0: (4, 4), 1: (5, 4), 2: (4, 5), 3: (6, 4), 4: (5, 5), 5: (4, 6),
                      6: (7, 4), 7: (6, 5), 8: (5, 6), 9: (4, 7)},
                     {0: (12, 0), 1: (12, 1), 2: (11, 1), 3: (12, 2), 4: (11, 2), 5: (10, 2),
                      6: (12, 3), 7: (11, 3), 8: (10, 3), 9: (9, 3)},
                     {0: (16, 4), 1: (15, 5), 2: (15, 4), 3: (14, 6), 4: (14, 5), 5: (14, 4),
                      6: (13, 7), 7: (13, 6), 8: (13, 5), 9: (13, 4)},
                     {0: (12, 12), 1: (11, 12), 2: (12, 11), 3: (10, 12), 4: (11, 11), 5: (12, 10),
                      6: (9, 12), 7: (10, 11), 8: (11, 10), 9: (12, 9)},
                     {0: (4, 16), 1: (4, 15), 2: (5, 15), 3: (4, 14), 4: (5, 14), 5: (6, 14),
                      6: (4, 13), 7: (5, 13), 8: (6, 13), 9: (7, 13)}
                    ]

        self.checkers_id = [None,
                    {(0, 12): 0, (1, 11): 1, (1, 12): 2, (2, 10): 3, (2, 11): 4, (2, 12): 5,
                     (3, 9): 6, (3, 10): 7, (3, 11): 8, (3, 12): 9},
                    {(4, 4): 0, (5, 4): 1, (4, 5): 2, (6, 4): 3, (5, 5): 4, (4, 6): 5,
                     (7, 4): 6, (6, 5): 7, (5, 6): 8, (4, 7): 9},
                    {(12, 0): 0, (12, 1): 1, (11, 1): 2, (12, 2): 3, (11, 2): 4, (10, 2): 5,
                     (12, 3): 6, (11, 3): 7, (10, 3): 8, (9, 3): 9},
                    {(16, 4): 0, (15, 5): 1, (15, 4): 2, (14, 6): 3, (14, 5): 4, (14, 4): 5,
                     (13, 7): 6, (13, 6): 7, (13, 5): 8, (13, 4): 9},
                    {(12, 12): 0, (11, 12): 1, (12, 11): 2, (10, 12): 3, (11, 11): 4, (12, 10): 5,
                     (9, 12): 6, (10, 11): 7, (11, 10): 8, (12, 9): 9},
                    {(4, 16): 0, (4, 15): 1, (5, 15): 2, (4, 14): 3, (5, 14): 4, (6, 14): 5,
                     (4, 13): 6, (5, 13): 7, (6, 13): 8, (7, 13): 9}
                   ]



        self.hist_moves = deque()

        if randomised:
            self.randomise_initial_state()

    def randomise_initial_state(self):
        '''
        Randomise the starting state of board
        '''
        self.board[:, :, 0] = 0
        position_list = [(row, col) for row in range(BOARD_HEIGHT) for col in range(BOARD_WIDTH)]

        # Randomly choose 12 positions and put checkers there
        chosen_indexes = np.random.choice(len(position_list), size=NUM_CHECKERS*2, replace=False)
        chosen_position = [position_list[i] for i in chosen_indexes]

        self.checkers_pos = [None, {}, {}]
        self.checkers_id = [None, {}, {}]

        # Take care to initialise the checkers_pos/checkers_id lookup table
        index = 0
        for player_num in [PLAYER_ONE, PLAYER_TWO]:
            for checker_id in range(NUM_CHECKERS):
                checker_pos = chosen_position[index]
                self.board[checker_pos][0] = player_num
                self.checkers_pos[player_num][checker_id] = checker_pos
                self.checkers_id[player_num][checker_pos] = checker_id
                index += 1

        assert index == NUM_CHECKERS * 2

    def check_win(self):
        """
        Returns the winner given the current board state; 0 if game still going
        To win:
            player 1: all checkers to upper right
            player 2: all checkers to lower left
        """
        cur_board = self.board[:, :, 0]
        one_win = two_win = True
        for k in range(BOARD_WIDTH - ROWS_OF_CHECKERS, BOARD_WIDTH):
            if one_win:
                up_diag = cur_board.diagonal(k)
                if not np.array_equal(up_diag, [PLAYER_ONE]*len(up_diag)):
                    one_win = False
            if two_win:
                down_diag = cur_board.diagonal(-k)
                if not np.array_equal(down_diag, [PLAYER_TWO]*len(down_diag)):
                    two_win = False

            if not one_win and not two_win:
                return 0

        return PLAYER_ONE if one_win else PLAYER_TWO

    def visualise(self, cur_player=None, gap_btw_checkers=3):
        """
        Prints the current board for human visualisation
        """
        print('=' * 75)
        print('Current Status:' + ' ' * 40 + 'Current Player: {}\n'.format(cur_player))

        cur_board = self.board[:, :, 0]        # Get current board from the topmost layer
        visual_width = BOARD_WIDTH * (gap_btw_checkers + 1) - gap_btw_checkers
        visual_height = BOARD_HEIGHT * 2 - 1    # Dimensions for visualisation
        leading_spaces = visual_width // 2

        for i in range(1, visual_height + 1):
            # Number of slots in the board row
            num_slots = i if i <= BOARD_WIDTH else visual_height - i + 1
            print('\tRow {:2}{}'.format(i, ' '*8), end='')
            # Print leading spaces
            print(' ' * ((leading_spaces - (num_slots - 1) * ((gap_btw_checkers + 1) // 2))), end='')
            diagonal_values = [str(val) if val != 9 else ' ' for val in cur_board.diagonal(BOARD_WIDTH - i)]
            print((' ' * gap_btw_checkers).join(diagonal_values), end='\n\n')  # Board contents
            # print((' ' * gap_btw_checkers).join(map(str, cur_board.diagonal(BOARD_WIDTH - i))), end='\n\n')  # Board contents

        print('=' * 75)

    def valid_checker_moves(self, cur_player, checker_pos):
        """
        Returns all valid moves for one checker piece
        """
        result = []
        # map to check already explored moves
        check_map = np.zeros((BOARD_WIDTH, BOARD_HEIGHT), dtype='uint8')
        # expand to each directions without jump
        result.append(checker_pos)
        check_map[checker_pos] = 1
        for walk_dir in self.directions:
            row, col = tuple(map(operator.add, checker_pos, walk_dir))
            if not board_utils.is_valid_pos(row, col):
                continue
            if self.board[row, col, 0] == 0:
                result.append((row, col))
                check_map[row, col] = 1

        # check continous jump moves
        self.board[checker_pos[0], checker_pos[1], 0] = 0;              # Remove current checker before checking
        self.valid_checker_jump_moves(result, check_map, checker_pos)
        self.board[checker_pos[0], checker_pos[1], 0] = cur_player;     # Put back current checker
        result.remove(checker_pos)                                      # Don't allow staying
        return result

    def valid_checker_jump_moves(self, valid_moves, check_map, checker_pos):
        """
        Add all recursive jumping moves into the list of valid moves
        """
        curr_row, curr_col = checker_pos
        # expand with jump
        for walk_dir in self.directions:
            step = 1
            row_inc, col_inc = walk_dir
            row, col = curr_row + row_inc, curr_col + col_inc
            valid_pos = True

            # Go along the direction to find the first checker and record steps
            while True:
                if not board_utils.is_valid_pos(row, col):
                    valid_pos = False
                    break
                if self.board[row, col, 0] != 0:
                    break
                step += 1
                row += row_inc
                col += col_inc

            if not valid_pos:
                continue

            # Continue in the direction to find the mirror move
            for i in range(step):
                row += row_inc
                col += col_inc
                if not board_utils.is_valid_pos(row, col) or self.board[row, col, 0] != 0:
                    valid_pos = False
                    break

            if not valid_pos:
                continue

            # get the row and col ready to jump
            # check whether the destination is visited
            if check_map[row, col] == 1:
                continue

            # store moves
            valid_moves.append((row, col))
            check_map[row][col] = 1
            self.valid_checker_jump_moves(valid_moves, check_map, (row, col))

    def get_valid_moves(self, cur_player):
        """
        Returns the collection of valid moves given the current player, in np indices
        """
        valid_moves_set = {}
        for checker_pos in self.checkers_pos[cur_player].values():
            valid_moves_set[checker_pos] = self.valid_checker_moves(cur_player, checker_pos)
        return valid_moves_set



    def place(self, cur_player, origin_pos, dest_pos):
        """
        Makes a move with array indices
        """
        # Make copy and make move
        cur_board = np.copy(self.board[:, :, 0])
        cur_board[origin_pos], cur_board[dest_pos] = cur_board[dest_pos], cur_board[origin_pos]

        # Move the checker in both id->positon and position->id lookup
        for checker_id, checker_pos in self.checkers_pos[cur_player].items():
            if checker_pos == origin_pos:
                self.checkers_pos[cur_player][checker_id] = dest_pos
                break

        self.checkers_id[cur_player][dest_pos] = self.checkers_id[cur_player].pop(origin_pos)

        # Update history
        self.board = np.concatenate((np.expand_dims(cur_board, axis=2), self.board[:, :, :BOARD_HIST_MOVES - 1]), axis=2)

        # Record history moves
        if len(self.hist_moves) == TOTAL_HIST_MOVES:
            self.hist_moves.popleft()
        self.hist_moves.append((origin_pos,dest_pos))

        return self.check_win()



    def player_progress(self, player_id):
        """
        Given player_id, return number of its checkers having reached the opponent's field.
        """
        cur_board = self.board[:, :, 0]
        diag_sign = player_id if player_id == PLAYER_ONE else -1
        reached_checkers_num = 0
        for k in range(BOARD_WIDTH - ROWS_OF_CHECKERS, BOARD_WIDTH):
            diag = cur_board.diagonal(diag_sign * k)
            for i in diag:
                if i == player_id:
                    reached_checkers_num += 1;
        return reached_checkers_num



    def player_forward_distance(self, player_id):
        """
        Given player_id, return the total forward distance its checkers went through.
        """
        cur_board = self.board[:, :, 0]
        checkers_pos = self.checkers_pos[player_id]
        distance = 0
        if player_id == PLAYER_ONE:
            distance = PLAYER_ONE_DISTANCE_OFFSET
            for _, pos in checkers_pos.items():
                row, _ = board_utils.np_index_to_human_coord(pos)
                distance -= row
        else:
            distance = PLAYER_TWO_DISTANCE_OFFSET
            for _, pos in checkers_pos.items():
                row, _ = board_utils.np_index_to_human_coord(pos)
                distance += row

        return distance

