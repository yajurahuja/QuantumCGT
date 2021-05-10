from graphics import *
from sys import*
from player import*
import numpy as np

class game:
	def __init__(self, size, winp, turn):
		self.boardsize = size
		self.win_parameter = winp
		self.turn = 1
		self.board = None # board matrix
		self.turn = 1
		self.moves = 0	
		self.tmoves = 9
		self.choice_info = ''
		self.players = []

	def addplayer(self):
		self.players.append(player(len(self.players) + 1, self))

	def setup(self):
		self.board = [[np.array([1.0,0.0,0.0]) for i in range(self.boardsize)] for j in range(self.boardsize)]
		

	def play(self):
		for i in range(self.tmoves):
			self.move()
		status = self.check_winner()
			if status == 1:
				print ("Player 1 wins")
				break
			elif status == 2:
				print ("Player 2 wins")
				break
			else:
			print("Draw")
			

	def move(self):
		print("Turn: Player " + str(self.turn))
		box_number, prob = self.players[self.turn - 1].move()
		for i in range(len(box_number)):
			row, column = (box_number[i] - 1)//3, (box_number[i] - 1)%3
			self.board[row][column][0] -= prob[i]
			self.board[row][column][self.turn] += prob[i]
		self.print_gameboard()
		self.turn = 3 - self.turn
		self.moves = self.moves + 1

	def check_winner(self):
		return 0

	def print_gameboard(self):
		print('\n\n\n')
		for row in self.board:
			print(row[0], row[1], row[2])
		print('\n\n\n')


	