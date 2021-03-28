# RL Project for interview.

 A tic tac toe agent that is trained with self play.

 Environment is compatible with OpenAI Gym structure.

 Environment folder contains env related functions.

 src folder contains RL Agent , Human test for testing environment capabilities and Agent's gym compatible interface.

 **State** is defined as game table + current marked('X' or 'O') info

 **Table** is defined as 1x9 table

 **Actions** are defined which area to play given moment. Defined as int.

 Rewards are defined accordingly question given. 
 
 To accomplish this I kept game status structure.

Draw is considered a winning (with reduced reward.)

Algorithm used is TD Learning with basic memory to keep tables/values. I felt no need for Deep Learning related method since it's pretty simple env.

Evaluation/Finding best agent is done with grid-search optimization.
I took inspiration how to implement a simple version of it.(grid-search opt)


As GUI i didnt do a web interface and OpenAI GYM gui seems decrepateced. Instead I 
opted for a dynamic command line interface with tqdm. 

It also shows / updates during agent training (process bar). 

## How to start ?

python  *anyfile in src.* should give you an output.

Agent is just to see if game works with given test inputs.

Human Agent is for testing game_functionality , breaking etc.

RL Agent needs a parameter to launch

Usage: rl_agent.py [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose  Increase verbosity.
  --help         Show this message and exit.

Commands:
  bench       Benchmark agent with base agent.
  gridsearch  Grid search hyper-parameters.
  learn       Learn and save the model.
  learnbench  Learn and benchmark.
  learnplay   Learn and play with human.
  play        Play with human.


