import numpy as np

# Fixed 2 player
PLAYER_ONE = 1
PLAYER_TWO = 2

ROWS_OF_CHECKERS = 3
BOARD_WIDTH = BOARD_HEIGHT = ROWS_OF_CHECKERS * 2 + 1
NUM_HIST_MOVES = 3      # Number of history moves to keep

class Board:
    def __init__(self):
        self._board = np.zeros((BOARD_WIDTH, BOARD_HEIGHT, NUM_HIST_MOVES), dtype='uint8')  # Initialize empty board
        self._board[:, :, 0] = np.array([[0, 0, 0, 0, 2, 2, 2],
                                         [0, 0, 0, 0, 0, 2, 2],
                                         [0, 0, 0, 0, 0, 0, 2],
                                         [0, 0, 0, 0, 0, 0, 0],
                                         [1, 0, 0, 0, 0, 0, 0],
                                         [1, 1, 0, 0, 0, 0, 0],
                                         [1, 1, 1, 0, 0, 0, 0]])


    @property
    def board(self):
        """
            Get the numpy array representing this board.
            Array is shaped 7x7x3, where the first 7x7 plane
            is the current board, while the latter are the
            two previous steps.
            PLAYER_ONE and PLAYER_TWO's checkers are initialised
            at bottom left and top right corners respectively.
        """
        return self._board


    def check_win(self):
        """ Returns the winner given the current board state; 0 if game still going """
        cur_board = self._board[:, :, 0]
        # to win:
        # 	player 1: go to upper right
        # 	player 2: 		lower left
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


    def print_board(self, gap_btw_checkers=5):
        """ Prints the current board for human visualisation """
        print('=' * 75)
        print('Current Status:')

        cur_board = self._board[:, :, 0]    # Get current board from the topmost layer
        visual_width = BOARD_WIDTH * (gap_btw_checkers + 1) - gap_btw_checkers
        visual_height = BOARD_HEIGHT * 2 - 1    # Dimensions for visualisation
        leading_spaces = visual_width // 2

        for i in range(1, visual_height + 1):
            # Number of slots in the board row
            num_slots = i if i <= BOARD_WIDTH else visual_height - i + 1
            print('\t\t\t', end='')
            # Print leading spaces
            print(' ' * ((leading_spaces - (num_slots - 1) * ((gap_btw_checkers + 1) // 2))), end='')
            print((' ' * gap_btw_checkers).join(map(str, cur_board.diagonal(BOARD_WIDTH - i))), end='\n\n')  # Board contents

        print('=' * 75)



    def valid_moves(self, cur_player):
        """ Returns the list of valid moves given the current player """
        # TODO: return a list of valid moves given the current players
        pass




if __name__ == '__main__':
    board = Board()

    # print(board.board)
    # board.print_board()
    # print(board.check_win())

    print(board.check_win())

    # for i in range(50000):
    # 	board.check_win()
