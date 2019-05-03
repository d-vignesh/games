

# implementing tic tac toe game using the Minimax algo and alpha beta pruning.

# logging module for debugging purpose
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# there will be two players 'x' and 'o'. 
# the moves of player 'x' will be chosen by the user 
# moves of player 'o' is the moves of the computer which will be determined by the minmax algo.



# implementing the func to return the best move the computer can choose with the given board configuration
# as were are finding the moves of the minimizer(i.e., computer which is the oponent) the find_best_move will try
# to find the min score that can be obtained with the given board state
# Note that winning score for user is +10 and winning score for the computer in -10

def find_best_move(board):
	best_val = 1000
	best_move = (-1, -1)
	alpha = -1000
	beta = 1000

	# given a board configuration , make all possible moves computer can make and evaluate the best move 
	for row in range(3):
		for col in range(3):
			if board[row][col] == '_':
				board[row][col] = 'o'
				cur_val = minmax(board, 0, True, alpha , beta)
				board[row][col] = '_'
				if cur_val < best_val:
					best_val = cur_val
					best_move = row, col

	return best_move

# implementing minmax algo to return the best value for a specific move chose by the computer
def minmax(board, depth , ismax, alpha, beta):

	score = evaluate(board)

	# if there is a winner 
	if score == 10 or score == -10:
		return score

	# if there is no move left in the board
	if not is_move_left(board):
		return 0

	if ismax:

		# the maximizing player make all possible move in the given board configuration
		# find the move that provides the highest value and return that value
		best_val = -1000
		for row in range(3):
			for col in range(3):
				if board[row][col] == '_':
					board[row][col] = 'x'
					cur_val = minmax(board, depth+1, False, alpha, beta)
					board[row][col] = '_'
					best_val = max(best_val, cur_val)

					# the alpha-beta pruning logic
					# the best value that a maximizer can make in this level is alpha or greater
					# the before turn in played by a minimizer which chooses the min value of its child
					# so if the alpha computed is greater than the already computed beta ( say from the left child and this is right child)
					# the previous minimizer player will sure choose the existing beta so there is no need to compute this level and its sub-levels
					alpha = max(best_val, alpha)
					if alpha >= beta :
						break
		return best_val

	else :
		# the minimizing player make all possible move in the given board configuration
		# find the move that provides the lowest value and return that value
		best_val = 1000
		for row in range(3):
			for col in range(3):
				if board[row][col] == '_':
					board[row][col] = 'o'
					cur_val = minmax(board, depth+1, True, alpha, beta)
					board[row][col] = '_'
					best_val = min(best_val, cur_val)

					# the alpha-beta pruning logic
					# the best value that the minimizer can make in this level is beta or lesser
					# the before turn is played by a maximizer which chooses the max value of its child
					# so if the beta computed is less than the already computed alpha( say from the left child)
					# the previous maximizer will sure choose the existing alpha so there is no need to compute this level and its sub-levels
					beta = min(beta, best_val)
					if beta <= alpha:
						break
		return best_val

# implementing the evaluation function to evaluate the score for current board state

def evaluate(board):

	# evaluate the score for the current board state
	# checking for row
	for row in range(3):
		if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
			if board[row][0] == 'x':
				return 10
			elif board[row][0] == 'o':
				return -10
	#logging.debug('no win in row')

	# checking for column
	for col in range(3):
		if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
			if board[0][col] == 'x':
				return 10
			elif board[0][col] == 'o':
				return -10
	#logging.debug('no win in col')

	# checking for diagonals
	if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
		if board[0][0] == 'x':
			return 10
		elif board[0][0] == 'o':
			return -10

	if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
		if board[0][2] == 'x':
			return 10
		elif board[0][2] == 'o':
			return -10

	# return 0 if no wins		
	return 0

# implementing the func to check for end of game 

def is_move_left(board):
	for i in range(3):
		for j in range(3):
			if board[i][j] == '_':
				return True
	return False

# creating the board layout and implementing the logic to populating the board by the inputs from the user

board = [
		  ['_', '_', '_'],
		  ['_', '_', '_'],
		  ['_', '_', '_']
		]
player = 1
won = False

while(is_move_left(board)):

	if player & 1:
		print('the state of the board is : ')
		print(board[0], board[1], board[2], sep='\n')

	score = evaluate(board)
	if score == 10 :
		print(' you won the game')
		won = True 
		break
	if score == -10 :
		print(' computer won the game')
		won = True
		break

	if player & 1 :

		# getting the index from the user
		# validating the index
		# placing the users move in the index
		while(True):
			row, col = map(int, input('enter the row and col were you wish to place : ').split(' '))
			if row >= 0 and row < 3 and col >=0 and col < 3 :
				if board[row][col] != '_':
					print('enter a position which is free')
				else:
					board[row][col] = 'x'
					break
			else:
				print('enter a valid position (0 >= row < 3) and (0 >= col < 3)')

	else :

		# this turn belongs to the computer
		# compute the best move the computer can make given the current board configuration
		row, col = find_best_move(board)
		board[row][col] = 'o'

	player = not(player)

if not won:
	print(board[0], board[1], board[2], sep='\n')
	print('the game is draw')

