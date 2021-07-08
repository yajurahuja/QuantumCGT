import sys
import numpy as np
import pickle

def getboardstr(board):
	boardstr = str(board.reshape(len(board) * len(board)))
	return boardstr

def get_winner(board, game_end = True, avail_pos = [1]):
	collapsed_board = board
	print(collapsed_board)
	p1 = 0
	p2 = 0
	d1 = []
	d2 = []
	#row_column check
	for i in range(len(collapsed_board)):
		p1, p2 = get_suite(collapsed_board[i ,:], p1, p2) #row
		p1, p2 = get_suite(collapsed_board[:,i], p1, p2) #column
	#diag check
	p1, p2 = get_suite(collapsed_board.diagonal() ,p1, p2)
	p1, p2 = get_suite(np.fliplr(collapsed_board).diagonal(), p1, p2)
	print(p1, p2)
	if(p1 > p2):
		return 1
	elif(p2 > p1):
		return 2
	elif len(avail_pos):
		if game_end == True:
			return 0
	else:
		return None


def get_suite(arr, p1, p2):
	arr = np.array(arr)
	result = np.all(arr == arr[0])
	if result:
		if(arr[0] == 1):
			p1 += 1
		elif(arr[0] == 2):
			p2 += 1
	return p1, p2

def avail_pos(board):
	positions = []
	for row in range(len(board)):
		for col in range(len(board)):
			if board[row][col] == 0:
				positions.append((row, col))
	return positions

#print the board
def showBoard(board):
	for i in range(len(board)):
		print('-------------')
		out = '| '
		for j in range(len(board)):
			if board[i, j] == 1:
				token = 'x'
			if board[i, j] == 2:
				token = 'o'
			if board[i, j] == 0:
				token = ' '
			out += token + ' | '
		print(out)
	print('-------------')


if __name__ == "__main__":
	board = np.array([[0, 2, 2],
				     [1, 1, 0], 
				     [0, 0, 0]])
	print(getboardstr(board))
	print(get_winner(board))
	print(avail_pos(board))
	print(showBoard(board))