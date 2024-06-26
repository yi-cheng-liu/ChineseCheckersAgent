import numpy as np
from collections import deque

from player import HumanPlayer, GreedyPlayer, AiPlayer
from board import Board
from config import *

class Game:
    def __init__(self, player_types=None, verbose=True, models=None, tree_tau=DET_TREE_TAU):
        if player_types is None:
            player_types = self.get_player_types()
        if models is None:
            models = [None] * 6

        self.players = []
        for i, p_type in enumerate(player_types):
            p_type = p_type[0].lower()
            if p_type == 'h':
                self.players.append(HumanPlayer(player_num=i + 1))
            elif p_type == 'g':
                self.players.append(GreedyPlayer(player_num=i + 1))
            else:
                self.players.append(AiPlayer(player_num=i + 1, model=models[i], tree_tau=tree_tau))

        self.cur_player_index = 0
        self.verbose = verbose
        self.board = Board()

    def get_player_types(self):
        player_types = []
        for i in range(6):
            while True:
                p_type = input(f'Enter player type of player {i + 1} ([H]uman/[G]reedyRobot/[A]I): ')
                if p_type[0].lower() in TYPES_OF_PLAYERS:
                    player_types.append(p_type)
                    break
                print('Invalid input. Try again.')
        return player_types
    
    def swap_players(self):
        self.cur_player_index = (self.cur_player_index + 1) % 6

    def start(self, enforce_move_limit=False):
        np.random.seed()
        total_moves = 0
        history_dests = deque()
        num_moves = 0
        while True:
            cur_player = self.players[self.cur_player_index]
            move_from, move_to = cur_player.decide_move(self.board, verbose=self.verbose, total_moves=total_moves)
            winner = self.board.place(cur_player.player_num, move_from, move_to)
            total_moves += 1
            if self.verbose:
                print('Total Moves:', total_moves)

            if winner:
                break

            if len(history_dests) == TOTAL_HIST_MOVES:
                history_dests.popleft()
            history_dests.append(move_to)

            cur_player_hist_dest = set([history_dests[i] for i in range(len(history_dests) - 1, -1, -6)])
            if len(history_dests) == TOTAL_HIST_MOVES and len(cur_player_hist_dest) <= UNIQUE_DEST_LIMIT:
                print('Repetition detected: stopping game')
                winner = None
                break

            num_moves += 1

            if enforce_move_limit and num_moves >= PROGRESS_MOVE_LIMIT:
                print('Game stopped by reaching progress move limit; Game Discarded')
                winner = None
                break

            self.swap_players()

        if self.verbose:
            self.board.visualise()

        if winner is not None:
            print('Player {} wins!'.format(winner))

        return winner

    # def __init__(self, p1_type=None, p2_type=None, verbose=True, model1=None, model2=None, tree_tau=DET_TREE_TAU):

    #     if p1_type is None or p2_type is None:
    #         p1_type, p2_type = self.get_player_types()

    #     p1_type = p1_type[0].lower()
    #     p2_type = p2_type[0].lower()

    #     if p1_type == 'h':
    #         self.player_one = HumanPlayer(player_num=1)
    #     elif p1_type == 'g':
    #         self.player_one = GreedyPlayer(player_num=1)
    #     else:
    #         self.player_one = AiPlayer(player_num=1, model=model1, tree_tau=tree_tau)

    #     if p2_type == 'h':
    #         self.player_two = HumanPlayer(player_num=2)
    #     elif p2_type == 'g':
    #         self.player_two = GreedyPlayer(player_num=2)
    #     else:
    #         self.player_two = AiPlayer(player_num=2, model=(model1 if model2 is None else model2), tree_tau=tree_tau)

    #     self.cur_player = self.player_one
    #     self.next_player = self.player_two
    #     self.verbose = verbose
    #     self.board = Board()


    # def get_player_types(self):
    #     p1_type = p2_type = ''
    #     while 1:
    #         p1_type = input('Enter player type of player 1 ([H]uman/[G]reedyRobot/[A]I): ')
    #         if p1_type[0].lower() in TYPES_OF_PLAYERS:
    #             break
    #         print('Invalid input. Try again.')

    #     while 1:
    #         p2_type = input('Enter player type of player 2 ([H]uman/[G]reedyRobot/[A]I): ')
    #         if p2_type[0].lower() in TYPES_OF_PLAYERS:
    #             break
    #         print('Invalid input. Try again.')

    #     return p1_type, p2_type


    # def swap_players(self):
    #     self.cur_player, self.next_player = self.next_player, self.cur_player


    # def start(self, enforce_move_limit=False):
    #     np.random.seed()
    #     total_moves = 0
    #     history_dests = deque()
    #     num_moves = 0
    #     while True:
    #         move_from, move_to = self.cur_player.decide_move(self.board, verbose=self.verbose, total_moves=total_moves)    # Get move from player
    #         winner = self.board.place(self.cur_player.player_num, move_from, move_to)  # Make the move on board and check winner
    #         total_moves += 1
    #         if self.verbose:
    #             print('Total Moves: {}'.format(total_moves))

    #         if winner:
    #             break

    #         if len(history_dests) == TOTAL_HIST_MOVES:
    #             history_dests.popleft()
    #         history_dests.append(move_to)

    #         # Impose repetition limit
    #         cur_player_hist_dest = set([history_dests[i] for i in range(len(history_dests) - 1, -1, -2)])
    #         if len(history_dests) == TOTAL_HIST_MOVES and len(cur_player_hist_dest) <= UNIQUE_DEST_LIMIT:
    #             print('Repetition detected: stopping game')
    #             winner = None
    #             break

    #         num_moves += 1

    #         if enforce_move_limit and num_moves >= PROGRESS_MOVE_LIMIT:
    #             print('Game stopped by reaching progress move limit; Game Discarded')
    #             winner = None
    #             break

    #         self.swap_players()


    #     if self.verbose:
    #         self.board.visualise()

    #     if winner is not None:
    #         print('Player {} wins!'.format(winner))

    #     return winner


if __name__ == '__main__':
    '''
    Ad hoc games
    '''
    from collections import Counter
    wincount = Counter()
    for i in range(10000):
        game = Game(p1_type='greedy', p2_type='greedy', verbose=False)
        game.player_two = GreedyPlayer(player_num=2, stochastic=True)
        wincount[game.start()] += 1
    print(wincount)

    '''
    Counter({1: 5172, 2: 4675, None: 153})
    Counter({1: 5233, 2: 4594, None: 173})
    determin wins 9908  stochastic wins 9766  draw 326
    '''




