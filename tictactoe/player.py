from graphics import *
from qiskit import *
from sys import*


class player:
	
	def __init__(self, number, game):
		self.player_number = number
		self.game = game

	def move(self, choice):
		print("choice" + str(choice))


class cplayer(player):

	def get_position(self):
		while True:
			x = int(input("Row: ")) - 1
			y = int(input("Column: ")) - 1
			if x >= 0 and x < self.game.boardsize and y >= 0 and y < self.game.boardsize:
				break
			else:
				print("Out of index")
		return x, y

	def cmove(self):
		row, column = self.get_position()
		index = row * self.game.boardsize + (column + 1)
		self.game.game_circuit.measure(index - 1, self.game.boardsize**2 - index)
		result=execute(self.game.game_circuit,backend=self.game.simulator,shots=1).result()
		circuit_array =list(result.get_counts(self.game.game_circuit).keys())[0]
		error_ = 0
		if index not in self.game.points:
			if circuit_array[index-1]=='1':
				self.game.game_circuit.reset(index-1)
				self.game.game_circuit.x(index-1)
				self.game.game_circuit.measure(index - 1, self.game.boardsize**2 - index)
			else:
				self.game.game_circuit.reset(index-1)
				self.game.game_circuit.measure(index - 1, self.game.boardsize**2 - index)
		else:
			global message
			print('Illegal move, Try again')
			error_ = 1

		self.game.points.append(index)
		self.game.update(index)
		return error_




	def move(self, choice):
		print("choice " + str(choice))
		self.cmove()

	

class qplayer(cplayer):

	def qmove(self):
		print("qmove")
	def hmove(self):
		print("reset")