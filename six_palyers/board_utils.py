from config import *

target_regions = {
            PLAYER_ONE: [(16, 4), (15, 5), (15, 4), (14, 6), (14, 5), (14, 4), (13, 7), (13, 6), (13, 5), (13, 4)],
            PLAYER_TWO: [(12, 12), (11, 12), (12, 11), (10, 12), (11, 11), (12, 10), (9, 12), (10, 11), (11, 10), (12, 9)],
            PLAYER_THREE: [(4, 16), (4, 15), (5, 15), (4, 14), (5, 14), (6, 14), (4, 13), (5, 13), (6, 13), (7, 13)],
            PLAYER_FOUR: [(0, 12), (1, 11), (1, 12), (2, 10), (2, 11), (2, 12), (3, 9), (3, 10), (3, 11), (3, 12)],
            PLAYER_FIVE: [(4, 4), (5, 4), (4, 5), (6, 4), (5, 5), (4, 6), (7, 4), (6, 5), (5, 6), (4, 7)],
            PLAYER_SIX: [(12, 0), (12, 1), (11, 1), (12, 2), (11, 2), (10, 2), (12, 3), (11, 3), (10, 3), (9, 3)]
        }

def np_index_to_human_coord(coord):
    np_i, np_j = coord
    human_row = np_i - np_j + BOARD_WIDTH
    human_col = min(np_i, np_j) + 1
    return human_row, human_col

def human_coord_to_np_index(coord):
    human_row, human_col = coord
    np_i = human_col - 1 + max(0, human_row - BOARD_WIDTH)
    np_j = human_col - 1 - min(0, human_row - BOARD_WIDTH)
    return np_i, np_j

def is_valid_pos(i, j):
    return i >= 0 and i < BOARD_HEIGHT and j >= 0 and j < BOARD_WIDTH

def convert_np_to_human_moves(np_moves):
    return { np_index_to_human_coord(key) : \
            [np_index_to_human_coord(to) for to in np_moves[key]] \
             for key in np_moves }

def heuristic_distance(start, end, player_num):
        """
        Calculate the heuristic distance based on the target positions.
        """
        start_dist = min([euclidean_distance(start, target) for target in target_regions[player_num]])
        end_dist = min([euclidean_distance(end, target) for target in target_regions[player_num]])
        return start_dist - end_dist

def euclidean_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.
    """
    return sum((x - y) ** 2 for x, y in zip(point1, point2)) ** 0.5


if __name__ == '__main__':
    """
    Put board_utils.py test cases here.
    """
    print(human_coord_to_np_index((13, 1)))
    print(human_coord_to_np_index((12, 1)))
    print(human_coord_to_np_index((10, 1)))
    print(human_coord_to_np_index((5, 3)))

    print(np_index_to_human_coord((6, 0)))
    print(np_index_to_human_coord((7, 1)))
