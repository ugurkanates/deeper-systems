# Reinforcement Learning Interview

The purpose of this task is to test your knowledge of reinforcement learning.

## Overview

The task is to implement a tic tac toe agent which learns how to play using reinforcement learning.

The rules are exactly standard, except:

* winning with a horizontal row is worth 3 points
* winning with any other 3-in-a-row (vertical or diagonal) is worth 1 point. 
* in the case of no three-in-a-rows (i.e. what would be a draw in standard rules), 
  the player with the most marks on the top row wins 0.5 points 

## Implementation

Your bot should be implemented in a module that implements this interface:

        def get_move(board, mark):
            '''
            * board should be a list of lists in row-column order with '' for empty, 'X' for X, and 'O' for O.
            * 'mark' is "X" if we are X, "O" if we are O.
            * return (row, column) of where to place the mark
            '''
            
That is, we should be able to use it like this:

    >>> from latest_bot import get_move
    >>> board = [['']*3 for _ in range(3)]
    >>> get_move(board, "X")  
    (1, 1)      # example only
    >>> board[1][1] = "X"
    >>> board[0][0] = "O"  # our move
    >>> get_move(board, "X")
    (0, 2)      # example only

This would mean your bot's first move is to place an X on the middle. We then place an O on top-left, and the bot
places an X on top-right.

## Deliverables

We need the following:

* Full source code including training script, along with any learned weights and the module as defined above which loads and plays with the best bot you made
* Human interface that we can use to play against the bot, either as X or as O. We want to see if we can personally beat the bot ourselves :). Inputting moves on command-line is ok, gym.openai graphical interface or any other web interface is extra credit
* Demo of the bot playing a fully random player along with expected value of it both as X and as O. The log of their
  gameplay should be visible and reasonably easy to follow. 
* Summary explaining how you implemented it, how you evaluated its performance, and what its performance is.



