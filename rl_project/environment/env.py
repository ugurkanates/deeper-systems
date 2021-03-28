import logging

import gym
from gym import spaces

CODE_MARK_MAP = {0: ' ', 1: 'O', 2: 'X'}
TABLE_SIZE = 9
HOR_REWARD = 3
DIAG_VERT_REWARD = 1
DRAW_REWARD = 0.5
NO_REWARD = 0
STATUS_MAP = {"WIN_HOR_CIRC":1,
              "WIN_HOR_X":2,
              "WIN_VERDIAG_CIRC":3,
              "WIN_VERDIAG_X":4,
              "DRAW_CIRC":5,
              "DRAW_X":6  }

LEFT_PAD = '  '



def tomark(code):
    # Used both for printing & marking code.
    if code in [ STATUS_MAP["WIN_VERDIAG_CIRC"], STATUS_MAP["DRAW_CIRC"] ]:
        code = STATUS_MAP["WIN_HOR_CIRC"]
    if code in [ STATUS_MAP["WIN_VERDIAG_X"] , STATUS_MAP["DRAW_X"] ]:
        code = STATUS_MAP["WIN_HOR_X"]
    
    return CODE_MARK_MAP[code]


def tocode(mark):
    return 1 if mark == 'O' else 2


def next_mark(mark):
    return 'X' if mark == 'O' else 'O'

def next_status(stat):
    # Status 3 = DIAG/VER win for O
    # Status 4 = DIAG/VER win for X
    return STATUS_MAP["WIN_VERDIAG_CIRC"] if stat == 1 else STATUS_MAP["WIN_VERDIAG_X"]


def agent_by_mark(agents, mark):
    for agent in agents:
        if agent.mark == mark:
            return agent


def after_action_state(state, action):
    """Execute an action and returns resulted state.

    Args:
        state (tuple): Board status + mark
        action (int): Action to run

    Returns:
        tuple: New state
    """

    board, mark = state
    nboard = list(board[:])
    nboard[action] = tocode(mark)
    nboard = tuple(nboard)
    return nboard, next_mark(mark)



def check_game_status(board):
    """Return game status by current board status.

    Args:
        board (list): Current board state

    Returns:
        int:
            -1: game in progress
            1: O winner for finished game. HOR
            2: X winner for finished game. HOR
            3: O winner for finished game. VER/DIAGO
            4: X winner for finished game. VER/DIAGO
            5: O draw winner 
            6: X draw winner
    """
    for t in [1, 2]:
        for j in range(0, 9, 3):
            if [t] * 3 == [board[i] for i in range(j, j+3)]:
                return t # horizon
        for j in range(0, 3): 
            if board[j] == t and board[j+3] == t and board[j+6] == t:
                return next_status(t) # vertical
        if board[0] == t and board[4] == t and board[8] == t:
            return next_status(t) # diag
        if board[2] == t and board[4] == t and board[6] == t:
            return next_status(t) # diag 

    for i in range(9):
        if board[i] == 0:
            # still playing
            return -1

    # draw game
    # determine winner by who has most on top row
    draw_circle = 0
    for i in range(0,3):
        if board[i] == 1:
            draw_circle += 1
    ret = STATUS_MAP["DRAW_CIRC"] if draw_circle == 2 else STATUS_MAP["DRAW_X"]

    return ret


class TicTacToeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, alpha=0.02, show_number=False):
        self.action_space = spaces.Discrete(TABLE_SIZE)
        self.observation_space = spaces.Discrete(TABLE_SIZE)
        self.alpha = alpha
        self.set_start_mark('O')
        self.show_number = show_number
        self.seed() 
        self.reset()

    def set_start_mark(self, mark):
        self.start_mark = mark

    def reset(self):
        self.board = [0] * TABLE_SIZE
        self.mark = self.start_mark
        self.done = False
        return self._get_obs()

    def step(self, action):
        """Step environment by action.

        Args:
            action (int): Location

        Returns:
            list: Obeservation
            int: Reward
            bool: Done
            dict: Additional information
        """
        assert self.action_space.contains(action)

        loc = action
        if self.done:
            return self._get_obs(), 0, True, None

        reward = NO_REWARD
        # place
        self.board[loc] = tocode(self.mark)
        status = check_game_status(self.board)
        reward = self._calculate_reward(status)
        logging.debug("check_game_status board {} mark '{}'"
                      " status {}".format(self.board, self.mark, status))



        # switch turn
        self.mark = next_mark(self.mark)
        return self._get_obs(), reward, self.done, None

    def _get_obs(self):
        return tuple(self.board), self.mark

    def render(self, mode='human', close=False):
        if close:
            return
        if mode == 'human':
            self._show_board(print)  
            print('')
        else:
            self._show_board(logging.info)
            logging.info('')

    def show_episode(self, human, episode):
        self._show_episode(print if human else logging.warning, episode)

    def _show_episode(self, showfn, episode):
        showfn("==== Episode {} ====".format(episode))

    def _show_board(self, showfn):
        """Draw tictactoe board."""
        for j in range(0, 9, 3):
            def mark(i):
                return tomark(self.board[i]) if not self.show_number or\
                    self.board[i] != 0 else str(i+1)
            showfn(LEFT_PAD + '|'.join([mark(i) for i in range(j, j+3)]))
            if j < 6:
                showfn(LEFT_PAD + '-----')

    def show_turn(self, human, mark):
        self._show_turn(print if human else logging.info, mark)

    def _show_turn(self, showfn, mark):
        showfn("{}'s turn.".format(mark))

    def show_result(self, human, mark, reward):
        self._show_result(print if human else logging.info, mark, reward)

    def _show_result(self, showfn, mark, reward):
        status = check_game_status(self.board)
        if status in [STATUS_MAP["WIN_HOR_CIRC"],STATUS_MAP["WIN_HOR_X"],
                    STATUS_MAP["WIN_VERDIAG_CIRC"],STATUS_MAP["WIN_VERDIAG_X"]]:
            msg = "Winner is '{}'!".format(tomark(status))
            showfn("==== Finished: {} ====".format(msg))
        elif status in [STATUS_MAP["DRAW_CIRC"],STATUS_MAP["DRAW_X"]]:
            msg = "Draw, due points winner is '{}'!".format(tomark(status))
            showfn("==== Finished: {} ====".format(msg))
        showfn('')

    def available_actions(self):
        return [i for i, c in enumerate(self.board) if c == 0]
    
    def _calculate_reward(self,status):
        if status >= 0:
            self.done = True
            if status in [STATUS_MAP["WIN_HOR_CIRC"], STATUS_MAP["WIN_HOR_X"]]:
                reward = HOR_REWARD if self.mark == 'O' else -HOR_REWARD
            if status in [STATUS_MAP["WIN_VERDIAG_CIRC"], STATUS_MAP["WIN_VERDIAG_X"]]:
                reward = DIAG_VERT_REWARD if self.mark == 'O' else -DIAG_VERT_REWARD
            if status in [STATUS_MAP["DRAW_CIRC"], STATUS_MAP["DRAW_X"]]:
                reward = DRAW_REWARD if self.mark == 'O' else -DRAW_REWARD
            return reward
        else:
            return 0

