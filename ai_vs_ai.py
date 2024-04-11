import re
import sys

from game import Game
from config import *
from model import *
from utils import find_version_given_filename
"""
Run this file with argument specifying the models from terminal if you
want to play ai-vs-ai game
e.g. python3 ai-vs-ai.py saved-models/version0000.h5 saved-models/version0033.h5
"""

def load_agent(model_path, model_num, verbose=False):
    model = ResidualCNN()
    model.version = utils.find_version_given_filename(model_path)
    if verbose:
        print('\nLoading model {} from path {}'.format(model_num, model_path))

    model.load_weights(model_path)

    if verbose:
        print('Model {} is loaded sucessfully\n'.format(model_num))

    return model


def agent_match(model1_path, model2_path, model3_path, model4_path, model5_path, model6_path, num_games, verbose=False, tree_tau=DET_TREE_TAU, enforce_move_limit=False):
    win_count = { PLAYER_ONE: 0, PLAYER_TWO: 0, PLAYER_THREE: 0 }

    model1 = load_agent(model1_path, 1, verbose)
    model2 = load_agent(model2_path, 2, verbose)
    model3 = load_agent(model3_path, 3, verbose)
    model4 = load_agent(model4_path, 4, verbose)
    model5 = load_agent(model5_path, 5, verbose)
    model6 = load_agent(model6_path, 6, verbose)

    for i in range(num_games):
        if verbose:
            utils.stress_message('Game {}'.format(i + 1))
        game = Game(p1_type='ai', p2_type='ai', p3_type='ai', p4_type='ai', p5_type='ai', p6_type='ai', verbose=verbose,
                    model1=model1, model2=model2, model3=model3, model4=model4, model5=model5, model6=model6, tree_tau=tree_tau)
        winner = game.start(enforce_move_limit=enforce_move_limit)
        if winner is not None:
            win_count[winner] += 1

    if verbose:
        print('Agent "{}" wins {} matches'.format(model1_path, win_count[PLAYER_ONE]))
        print('Agent "{}" wins {} matches'.format(model2_path, win_count[PLAYER_TWO]))
        print('Agent "{}" wins {} matches'.format(model3_path, win_count[PLAYER_THREE]))
        print('Agent "{}" wins {} matches'.format(model4_path, win_count[PLAYER_FOUR]))
        print('Agent "{}" wins {} matches'.format(model5_path, win_count[PLAYER_FIVE]))
        print('Agent "{}" wins {} matches'.format(model6_path, win_count[PLAYER_SIX]))

    # Return the winner by at least 20% win rate
    if win_count[PLAYER_ONE] > int(0.2 * num_games):
        return model1_path
    elif win_count[PLAYER_TWO] > int(0.2 * num_games):
        return model2_path
    elif win_count[PLAYER_THREE] > int(0.2 * num_games):
        return model3_path
    elif win_count[PLAYER_FOUR] > int(0.2 * num_games):
        return model1_path
    elif win_count[PLAYER_FIVE] > int(0.2 * num_games):
        return model2_path
    elif win_count[PLAYER_SIX] > int(0.2 * num_games):
        return model3_path
    else:
        return None


if __name__ == '__main__':
    if len(sys.argv) < 7:
        print('Usage: python3 ai-vis-ai.py <models_path> [<tree tau>]')
        exit()

    if len(sys.argv) == 7:
        agent_match(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], 1, True)
    else:
        tree_tau = float(sys.argv[7])
        utils.stress_message('Using tree_tau {} initially'.format(tree_tau))
        agent_match(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], 1, True, tree_tau)
