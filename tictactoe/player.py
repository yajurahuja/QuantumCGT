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

			if index in self.game.control_positions.keys():
				for target in self.game.control_positions[index]:
					self.game.game_circuit.cx(index-1,target-1)
				for target in self.game.control_positions[index]:
					self.game.game_circuit.measure(target - 1, self.game.boardsize**2 - target)

		else:
			global message
			print('Illegal move, Try again')
			error_ = 1

		self.game.points.append(index)
		self.game.update(index)
		return error_




	def move(self, choice):
		print("choice " + str(choice))
		if choice == 1:
			self.cmove()
		elif choice == 2 or choice == 3:
			print("Cannot make a quantum move")
		else:
			print("wrong choice")


class qplayer(cplayer):

	def qmove(self):
		print("Enter for Target Bit")
		row, column = self.get_position()
		targetbit = (row * self.game.boardsize) + (column + 1)

		print("Enter for Control Bit")
		row, column = self.get_position()
		controlbit = (row * self.game.boardsize) + (column + 1)


		if targetbit in self.game.points and controlbit not in self.game.points:
			
			if targetbit in self.game.target_positions.keys():
				self.game.target_positions[targetbit].append(controlbit)
			else:
				self.game.target_positions[targetbit] = [controlbit]

			if controlbit in self.game.control_positions.keys():
				self.game.control_positions[controlbit].append(targetbit)
			else:
				self.game.control_positions[controlbit] = [targetbit]
			print(controlbit,'-',targetbit,' ',"entangled")
			return 0
		else :
			global message
			print('Illegal move')
			return 1

	def hmove(self):
		row, column = self.get_position()
		index = row * self.game.boardsize + (column + 1)
		if index in self.game.points and index not in self.game.target_positions.keys():
			self.game.game_circuit.reset(index - 1)
			self.game.game_circuit.h(index - 1)
			self.game.points.remove(index)
			self.game.board[row][column] = 0
			return 0
		else:
			global message
			print('Illegal move, Try again')
			return 1

	def move(self, choice):
		print("choice " + str(choice))
		if choice == 1:
			self.cmove()
		elif choice == 2:
			self.qmove()
		elif choice == 3:
			self.hmove()
		else:
			print("wrong choice")



