1. Name: Nolan Donaldson 10754467

2. Python 3

3. The code is split between two python scripts akin to the starter code. In the file
   maxconnect4.py, there are 3functions. The first one handles a single move of the
   game for one-move mode. The second handles the interactive gamemode between the AI
   and a human player. Last, is main, which handles the command line arguments and runs
   the game.

   In the next file, MaxConnect4Game.py, there is a class called maxconnect4 that consists of
   the main game logic. It has 6 variables, the board, whose turn it is, the scores of each player,
   the number of pieces on the board, and the name of the output file. There are also 10 methods.
   The first counts how many pieces are on the board, the second prints the board, the third 
   writes the board to a file (in the same format as the input files), the fourth places a piece
   on the board (it will return 0 if it an invalid space and return 1 if it is valid), the fifth
   and sixth assign utilty values to piece combinations on the board, the seventh runs a a depth-
   limited minimax search with alpha-beta pruning on the board to determine a good spot for the AI
   to place a piece, the next two methods help the minimax algorithm run, and the last method scores
   each player for their performance in the game.

4. To run the program, assuming on a windows 10 machine, navigate to the directory that both of the 
   scripts are in. Make sure the desired input files are also in this directory. As the program consists 
   of python scripts, no prior compilation is required. Then, enter a command with the following format:

   python3 maxconnect4 [GAME_MODE] [INPUT_FILE] [OUTPUT_FILE] [DEPTH]

   for example, to play a game of the AI against itself with a depth of 5, one would enter:

   python3 maxconnect4 one-move input1.txt output1.txt 5

   to run in interactive mode, as a human against the AI, with a depth of 3 and using the files input1.txt
   as input and output45.txt as output, use:

   python3 maxconnect4 interactive input1.txt output45.txt 3

   These above steps may also be followed on a linux shell such as Ubuntu. Also, if the python3 keyword does not 
   work in powershell, one may also use the format:

   & [PATH_TO_PYTHON_3_EXECUTABLE] "[PATH_TO_PROJECT_FOLDER]" [GAME_MODE] [INPUT_FILE] [OUTPUT_FILE] [DEPTH]

   Here is an example (from my machine, your paths will vary):

   & C:/Users/nmdon/AppData/Local/Programs/Python/Python38-32/python.exe "z:/AI/Project 2/maxconnect4.py" one-move input2.txt output.txt 6