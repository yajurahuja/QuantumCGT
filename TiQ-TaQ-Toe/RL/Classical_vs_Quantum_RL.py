import numpy as np
from scipy import sparse
import itertools


import random
from collections import Counter
import functools
import operator
import pickle
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister, execute
from qiskit import BasicAer


BOARD_ROWS = 3
BOARD_COLS = 3

ampcombinations = [[1, 0], [1/np.sqrt(2), 1/np.sqrt(2)]]


class Game:
	def __init__(self, player1, player2):
		self.p1 = player1
		self.p2 = player2
		self.gameEnd = False
		self.turn = 1
		self.moves = 0
		self.gameboards = [[1,'000000000']]

	def initial_board(self):
		"""This is the initial board with amplitude 1 and 0s in all the places"""
		return [[1,'000000000']]

	def avaialable_positions(self, board):
		"""Given a board and a players whose turn it is, this method returns a set of 
		all positions on the board that player can make on the board"""
		positions = []
		for i in range(BOARD_ROWS):
			for j in range(BOARD_COLS):
				if board[(3 * i) + j] == '0':
					positions.append((i,j))
		return positions

	def getReward(self):
		"""After a game is finished, this method feeds the appropriate reward to the players"""
		sum_p1, sum_p2 = self.getResult()
		print("rewards -  P1: " + str(sum_p1) +' P2: '+ str(sum_p2))
		self.p1.feedReward(sum_p1)
		self.p2.feedReward(sum_p2)
		self.p1.reward_list.append(sum_p1)
		self.p2.reward_list.append(sum_p2)

		# if result == 1:
		# 	self.p1.feedReward(1)
		# 	self.p2.feedReward(0)
		# elif result == 2:
		# 	self.p1.feedReward(0)
		# 	self.p2.feedReward(1)
		# else:
		# 	self.p1.feedReward(0.1)
		# 	self.p2.feedReward(0.1)

	def reset(self):
		"""Resets all members of the game after each time it has been played"""
		self.gameEnd = False
		self.turn = 0
		self.moves = 0
		self.gameboards = self.initial_board()

	def status(self, one_board):
		"""This returns 1 if the the player won this board, -1 is opponent won and 0 if it's a draw"""
		player_number = '1'
		zeros = [k for k in range(len(one_board)) if one_board.startswith('0', k)]
		opponent_number='2' if player_number=='1' else '2'

		diags = [[one_board[0],one_board[4],one_board[8]],[one_board[2],one_board[4],one_board[6]]]
		rows = [[one_board[0],one_board[1],one_board[2]],[one_board[3],one_board[4],one_board[5]],[one_board[6],one_board[7],one_board[8]]]
		cols =[[one_board[0],one_board[3],one_board[6]],[one_board[1],one_board[4],one_board[7]],[one_board[2],one_board[5],one_board[8]]]
		combined = diags + rows + cols

		if(len(zeros)==0):
			if(any(i.count(player_number)==3 for i in combined) and all(i.count(opponent_number)!=3 for i in combined)):
				return 1
			elif (any(i.count(opponent_number)==3 for i in combined) and all(i.count(player_number)!=3 for i in combined)):
				return 2
			else:
				return 0	

	def getResult(self):
		sum_p1 = 0
		sum_p2 = 0
		for i, j in self.gameboards:
			result = self.status(j)
			if result == 1:
				sum_p1 += abs(i**2) * 100
			elif result == 2:
				sum_p2 += abs(i**2) * 100
		return sum_p1, sum_p2


	def play(self, rounds = 100):
		""" The user enters the number of rounds and the game is played than many number of times"""
		for i in range(rounds):
			print('\n\n\n')
			print("Rounds " + str(i))
			while not self.gameEnd:
				positions = []
				self.moves += 1
				#print("Move: " + str(self.moves))
				if self.moves % 2 == 1:
					player = self.p1
				else:
					player = self.p2

				#print("gameboards: " + str(len(self.gameboards)))
				#print(self.gameboards)
				for board in self.gameboards:
					positions.append(self.avaialable_positions(board[1]))
				actions, amps = player.chooseAction(positions, self.gameboards)
				self.gameboards = Game.move(self.gameboards, actions, amps, player.number)
				board_hash = getHash(self.gameboards)
				player.addState(board_hash)
				self.turn = 3 - self.turn
				#print('turn ' + str(self.turn))
				if(self.moves == 9):
					self.gameEnd = True
			#print("Final Gameboards: " + str(len(self.gameboards)))
			#print(self.gameboards)
			self.getReward()
			self.p1.reset()
			self.p2.reset()
			self.reset()


	@staticmethod
	def move(gameboards, actions, amps, player_number):
		""" Given a the current game state that is the set of gameboards, actions 
		that is the zeros chosen and the amplituted, this method performs the move on the game state 
		and returns the new set of gameboards"""

		new_board = []
		for n in range(len(gameboards)):
			i = gameboards[n][0]
			j = gameboards[n][1]
			zeros = [k for k in range(len(j)) if j.startswith('0', k)]
			if (len(zeros)>= 2):
				amp = amps[n]
				#print(amp)
				#print(actions[n])
				chosen_zeros = []
				for action in actions[n]:
					(a, b) = action
					chosen_zeros.append(a*3 + b)
				#print("data")
				#print(amp, chosen_zeros)
				new_amplitudes = [round((element*i).real,2)+round((element*i).imag,2)*1j for element in amp]
				new_positions = []
				for index in chosen_zeros:
					new_positions.append(j[:index] + str(player_number) + j[index + 1:])
				current_board = [list(a) for a in zip(new_amplitudes, new_positions)]
				new_board.extend(current_board)
				#print('Initital:',i,j,'\nRandom Apms: ', amp, '\nRandom Positions: ',chosen_zeros,'\nNew Apms: ',new_amplitudes, '\nNew Positions: ',new_positions, '\nCurrent Board: ',current_board,'\n\n\n')
			elif (len(zeros)==1):
				for index in zeros:
					new_positions = j[:index] + str(player_number) + j[index + 1:]
				current_board = [[i, new_positions]]
				new_board.extend(current_board)
			else:
				new_board = board 
		flat = functools.reduce(operator.iconcat, new_board, [])
		duplicate_items = ([item for item, count in Counter(flat).items() if (count > 1 and type(item)==str)])

		concatenated_list = []
		all_indexes = []
		for i in duplicate_items:
			indexes = []
			for j in new_board:
				if (i==j[1]):
					indexes.append(new_board.index(j))
					all_indexes.append(new_board.index(j))
			total_amp = 0
			for k in indexes:
				total_amp += new_board[k][0]
			combined_ele = [total_amp,i]
			concatenated_list.append(combined_ele)

		for ele in sorted(all_indexes, reverse = True): 
				del new_board[ele]   
		new_board.extend(concatenated_list)

		#Eliminating boards with no amplitude 
		unwanted = []
		for i in new_board:
			if(i[0]==False):
				unwanted.append(new_board.index(i))
		for ele in sorted(unwanted, reverse = True): 
			del new_board[ele]

		#Re-normalizing the board
		a,b = map(list, zip(*new_board))
		a = np.array(a)
		a = list(a/np.linalg.norm(a))

		new_board = [list(i) for i in zip(a,b)] 
		return new_board


class player:
	def __init__(self, number, type_, exp_rate = 0.3):
		self.number = number
		self.states = []
		self.lr = 0.2
		self.exp_rate = exp_rate
		self.decay_gamma = 0.9
		self.classicalstate_values = None
		self.states_values = {} # state -> value
		self.game = None
		self.type = type_
		self.reward_list = []

	def chooseAction(self, positions, gameboards):
		if self.type == 'c':
			actions, amps = self.chooseActionC(positions, gameboards)
		elif self.type == 'q':
			actions, amps = self.chooseActionQ(positions, gameboards)
		return actions, amps


	def chooseActionQ(self, positions, gameboards):
		#fullamps = [1, -1 , 1j, -1j]
		#halfamps = [1/np.sqrt(2), -1/np.sqrt(2), 1j/np.sqrt(2), -1j/np.sqrt(2)]
		#totalamps = []
		if np.random.uniform(0, 1) <= self.exp_rate:

			idx = [np.random.choice(len(position), size = 2, replace = False) if len(position) >= 2 else np.random.choice(len(position), size = 2, replace = True) for position in positions]
			actions = [np.array(positions[i])[idx[i]] for i in range(len(positions))]
			max_amps = []
			for action in actions:
					index =  np.random.choice(2)
					amp = ampcombinations[index]
					max_amps.append(amp)
		else: 
			actions = []
			amplist = []
			for i in range(len(gameboards)):
				a1, a2 = self.choose2ActionC(positions[i], gameboards[i][1])
				actions.append([a1, a2])
			subsets = sub_lists(list(range(len(gameboards))))
			for subset in subsets:
				amps = []
				for i in range(len(gameboards)):
					amps.append(ampcombinations[0])
				for i in subset:
					amps[i] = ampcombinations[1]
				amplist.append(amps)
			max_value = -999
			max_amps = None
			for amps in amplist:
				new_board = Game.move(gameboards, actions, amps, self.number)
				new_boardhash = getHash(new_board)
				if self.states_values.get(new_boardhash) is None:
					value = 0
				else:
					value = self.states_values.get(new_boardhash)
				if value >= max_value:
					max_value = value
					max_amps = amps
		print("Q move")
		print(len(self.states_values))
		print(actions, max_amps)
		return actions, max_amps

	def chooseActionC(self, positions, gameboards):
		actions = []
		amps = []

		if np.random.uniform(0, 1) <= self.exp_rate:
			for i in range(len(gameboards)):
				a = np.random.choice(len(positions[i]), size = 2, replace = False) if len(positions[i]) >= 2 else np.random.choice(len(positions[i]), size = 2, replace = True)
				b = []
				for j in a:
					b.append(positions[i][j])
				actions.append(b)
				amps.append([1, 0])


		else:
			for i in range(len(gameboards)):
				actions.append(self.choose2ActionC(positions[i], gameboards[i][1]))
				amps.append([1, 0])
		print("C move")
		print(actions, amps)
		return actions, amps

	def choose2ActionC(self, positions, gameboard):
		max_1 = -999
		a1 = None
		max_2 = -999
		a2 = None
		for i,j in positions:
			index = 3*i + j
			next_board = gameboard
			next_board = next_board[:index] + str(self.number) + next_board[index + 1:]
			next_board = getHashC(next_board)
			if self.classicalstate_values.get(next_board) is None:
				value = 0
			else: 
				value = self.classicalstate_values.get(next_board)
			#print(value)

			if value >= max_1:
				max_2 = max_1
				a2 = a1
				max_1 = value
				a1 = (i,j)

			elif value >= max_2:
				max_2 = value
				a2 = (i,j)
		return [a1, a2] 

	def choose1ActionC(self, positions, gameboard):
		max_ = -9999
		action= None
		for i,j in positions:
			index = 3*i + j
			next_board = gameboard
			next_board = next_board[:index] + str(self.number) + next_board[index + 1:]
			next_board = getHashC(next_board)
			if self.classicalstate_values.get(next_board) is None:
				value = 0
			else: 
				value = self.classicalstate_values.get(next_board)	
				if value >= max_:
					max_ = value
					action = (i, j)

		return a1

	def addState(self, state):
		self.states.append(state)

	def feedReward(self, reward):
		for st in reversed(self.states):
			if self.states_values.get(st) is None:
				self.states_values[st] = 0
			self.states_values[st] += self.lr * (self.decay_gamma * reward - self.states_values[st])
			reward = self.states_values[st]

	def reset(self):
		self.states = []

	def savePolicy(self):
		fw = open('Qpolicy_' + str(self.number), 'wb')
		pickle.dump(self.states_values, fw)
		fw.close()

	def loadPolicy(self, file):
		fr = open(file, 'rb')
		self.classicalstate_values = pickle.load(fr)
		fr.close()

	def setGame(self, game):
		self.game = game




"""The following below are the utility functions"""

def sub_lists(l):
    lists = [[]]
    for i in range(len(l) + 1):
        for j in range(i):
            lists.append(l[j: i])
    return lists

def getHash(gameboards):
	q0 = np.array([1, 0, 0])
	q1 = np.array([0, 1, 0])
	q2 = np.array([0, 0, 1])
	l = []
	for i in gameboards:
		tensor_product = np.array([1])
		for j in i[1]:
			if(j == '0'):
				tensor_product = np.kron(tensor_product, q0)
			elif(j == '1'):
				tensor_product = np.kron(tensor_product, q1)
			elif(j == '2'):
				tensor_product = np.kron(tensor_product, q2)
		i1 = list(tensor_product).index(1)
		i2 = i[0]
		l.append([i2, i1])
	statevector = [0] * (3**9)
	for i,j in l:
		statevector[j] = i
	normalised = statevector/np.linalg.norm(statevector)

	hash = str(sparse.csr_matrix(normalised))
	return hash

def getHashC(board):
	b = np.zeros((BOARD_ROWS, BOARD_COLS))
	for i in range(BOARD_ROWS):
		for j in range(BOARD_COLS):
			idx = 3 * i + j
			if board[idx] == '1':
				b[i][j] = 1
			elif board[idx] == '2':
				b[i][j] = -1 
	#print(b)
	return str(b.reshape(BOARD_ROWS * BOARD_COLS))

def plot(p1, p2):
	plt.plot(p1.reward_list, label = ['p1 '  + p1.type])
	plt.plot(p2.reward_list, label = ['p2 '  + p2.type])
	plt.title("Rewards Graph")
	plt.ylabel('reward')
	plt.xlabel('iterations')
	plt.legend()
	plt.show()


if __name__ == '__main__':
	Q = player(1, 'q', 0.3)
	Q.loadPolicy('policy_p1')
	C = player(2, 'q', 0.3) 
	C.loadPolicy('policy_p2')
	G = Game(Q, C)
	Q.setGame(G)
	C.setGame(G)
	G.play(100)
	print(Q.states_values)
	plot(Q, C)
	#Q.savePolicy()

