from QuantumBoard import *
from gui import *

amplitudes = np.array([0, 1, -1 , 1j, -1j, 1/np.sqrt(2), -1/np.sqrt(2), 1j/np.sqrt(2), -1j/np.sqrt(2)], dtype = complex)
amplitudes = {'0': 0, '1': 1, '-1': -1, 'i': 1j , '-i': -1j , '1/\u221A2': 1/np.sqrt(2), '-1/\u221A2': -1/np.sqrt(2), 'i/\u221A2': 1j/np.sqrt(2), '-i/\u221A2':  -1j/np.sqrt(2)}


class player:

	def __init__(self, number, name):
		self.player_number = number
		self.player_name = name


	def move(self, gameboard, move, current_board, widget, app):
		boardlist = gameboard.get_boards()
		amplist = gameboard.get_elements()
		widget.addWidget(TicTacToeWindow(widget, self, move, boardlist, current_board, amplist))
		widget.setCurrentIndex(widget.currentIndex() + 1)
		widget.show()
		app.exec()
		boards, boxes, amps = widget.currentWidget().return_data()
		for i in range(len(amps)):
			amps[i] = amplitudes[amps[i]]
		gameboard.apply_unitary_9(self.player_number, gameboard.create_unitary(self.player_number, boards, boxes, amps))
		gameboard.set_move(move)


	def move_9(self, gameboard, move):
		print("Turn: Player " + str(self.player_number), "Move: " + str(move))
		print("1 : 0, 2 : 1, 3 : -1 , 4 : i, 5 : -i, 6 : 1/np.sqrt(2), 7 : -1/sqrt(2), 8 : i/sqrt(2), 9 : -i/sqrt(2)")
		boards = []
		boxes = []
		amps = []
		boardstr = gameboard.get_boards()
		for board in boardstr:
			print("Enter input for board: " + board)
			inp = input("Enter first box numbers (1-9) and the amplitude index from the list: ")
			inp = inp.split(' ')
			boards.append(board)
			boxes.append(int(inp[0])-1)
			amps.append(amplitudes[int(inp[1])-1])
			inp = input("Enter second box numbers (1-9) and the amplitude index from the list or e for not entering more prob: ")
			if inp == 'e':
				continue
			else:
				inp = inp.split(' ')
				boards.append(board)
				boxes.append(int(inp[0])-1)
				amps.append(amplitudes[int(inp[1])-1])
		gameboard.apply_unitary_9(self.player_number, gameboard.create_unitary(self.player_number, boards, boxes, amps))
		gameboard.set_move(move)




	#def move(self):
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


	# def move(self, board, move):
	# 	print("Turn: Player " + str(self.player_number), "Move: " + str(move))
	# 	inp = input("Enter 2 box numbers (1-9) with spaces: ")
	# 	inp = inp.split(' ')
	# 	prob = input("input probability of first box: ")
	# 	rad = 2 * np.arccos(np.sqrt(float(prob)))
	# 	self.U(board, int(inp[0])- 1 , int(inp[1]) - 1, rad) 
	# 	#self.EQ(board, int(inp[0])- 1 , int(inp[1]) - 1) 
	# 	board.set_move(move)




	# def EQ(self, board, q1, q2):
	# 	gindex = '0' + str(self.player_number)
	# 	board.apply_unitary_1(self.player_number, H[gindex], q1)
	# 	board.apply_unitary_1(self.player_number, X[gindex], q2)
	# 	board.apply_unitary_controlled(self.player_number, X[gindex], q1, q2)

	# def U(self, board, q1, q2, rad):
	# 	gindex = '0' + str(self.player_number)
	# 	board.apply_unitary_1(self.player_number, X[gindex], q1)
	# 	board.apply_unitary_1(self.player_number, R_y(rad, gindex), q2)
	# 	board.apply_unitary_controlled(self.player_number, X[gindex], q2, q1)
