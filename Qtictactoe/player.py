from QuantumBoard import *


class player:

	def __init__(self, number):
		self.player_number = number

	def move(self, board, move):
		print("Turn: Player " + str(self.player_number), "Move: " + str(move))
		inp = input("Enter 2 box numbers (1-9) with spaces: ")
		inp = inp.split(' ')
		self.EQ(board, int(inp[0])- 1 , int(inp[1]) - 1)
		board.set_move(move)

	def strategy(self, board):

		return U

	def move_input(self):
		print("Please input box number: ")
		inp = int(input())
		return inp

	def EQ(self, board, q1, q2):
		board.apply_unitary_1(self.player_number, H['01'], q1)
		board.apply_unitary_1(self.player_number, X['01'], q2)
		board.apply_unitary_controlled(self.player_number, X['01'], q2, q1)


	# def move(self):
	# 	print("Please input as box number(1-9) probability(0-1) and press enter. type d and press enter to end turn.")
	# 	box_number = []
	# 	prob = []
	# 	while True:
	# 		inp = input()
	# 		if (inp == 'd'):
	# 			break
	# 		inp = inp.split(' ')
	# 		print(inp)
	# 		box_number.append(int(inp[0]))
	# 		prob.append(float(inp[1]))
	# 	print(box_number, prob)
	# 	if(sum(prob) != 1):
	# 		print("Error: probability sum not equal to 1")
	# 		return self.move()
	# 	else:
	# 		for i in range(len(box_number)):
	# 			row, column = (box_number[i] - 1)//3, (box_number[i] - 1)%3
	# 			if(prob[i] > self.game.board[row][column][0]):
	# 				print("Error: probability entered is more than empty")
	# 				return self.move()
	# 	return box_number, prob




