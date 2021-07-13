import numpy as np
import pickle

import random
from collections import Counter
import functools
import operator

from qiskit import QuantumCircuit, QuantumRegister, execute
from qiskit import BasicAer

BOARD_ROWS = 3
BOARD_COLS = 3

class State:
	def __init__(self, player1, player2):
		self.gameboards = None
		self.p1 = player1
		self.p2 = player2 
		self.gameEnd = False
		self.turn = 1
		self.move = 0

	def initial_board()
		return [[1, '000000000']]

	def winner(one_board):
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

	def availablePositions(self, board, player):
		positions = []
		for i in range(BOARD_ROWS):
			for j in range(BOARD_COLS):
				if board[(3 * i) + j] == '0':
					positions.append((i,j))
		return positions


	def getReward(self):
		result = self.winner()
		if result == 1:
			self.p1.feedReward(1)
			self.p2.feedReward(0)
		elif result == 2:
			self.p1.feedReward(0)
			self.p2.feedReward(1)
		else:
			self.p1.feedReward(0.1)
			self.p2.feedReward(0.1)

	def reset(self):
		self.board = None
		self.board = None
		self.gameEnd = False
		self.turn = 0

	def getHash(self, gameboard):
		q0 = np.array([1, 0, 0])
		q1 = np.array([0, 1, 0])
		q2 = np.array([0, 0, 1])
		l = []
		for i in gameboard:
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



	def play(self, rounds = 100):
		for i in range(rounds):
			if i % 1000 == 0:
				print("Rounds " + str(rounds))
			while not self.gameEnd:
				positions = []
				self.move += 1
				if self.move % 2 == 1:
					player = self.p1
				else:
					player = self.p2

				for board in self.gameboards:
					positions.append(self.availablePositions(board[1], player))
				action = player.chooseAction(positions, self.board, (self.turn))
				self.updateState(action)
				board_hash = self.getHash()
				player1.addState(board_hash)
				if(self.turn == 9)
					self.gameEnd = True
			win = self.winner()
			self.getReward()
			self.p1.reset()
			self.p2.reset()
			self.reset()
			self.turn = 3 - self.turn


class player:
	def __init__(self, number, cstate_values, exp_rate = 0.3):
		self.name = str(number)
		self.states = []
		self.lr = 0.2
		self.exp_rate = exp_rate
		self.decay_gamma = 0.9
		self.classicalstate_values = cstate_values
		self.state_values = {} # state -> value

	def chooseAction(self, positions, current_board, turn):

	def chooseCAction(self, positions, current_board, turn):
		if np.random.uniform(0, 1) <= self.exp_rate:
			idx = np.random.choice(len(positions), size = 2)
			action1, action2 = positions[idx[0]], positions[idx[1]]
		else: 
			max_1 = -999
			a1 = None
			max_2 = -999
			a2 = None
			for i,j in positions:
				index = 3*i + j
				next_board = current_board.copy()
				next_board = next_board[:index] + str(turn) + next_board[index + 1:]
				if self.classicalstate_values.get(next_board) is None:
					value = 0
				else: 
					value = self.classicalstate_values.get(next_board)

				if value >= max_1:
					max_2 = max_1
					a2 = a1
					max_1 = value
					a1 = (i,j)

				elif value >= max_2:
					max_2 = value
					a2 = (i,j)
		return a1, a2 

	def addState(self, state):
		self.states.append(state)

	def feedReward(self, reward):
		for st in reversed(self.states):
			if self.states_value.get(st) is None:
				self.states_value[st] = 0
			self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
			reward = self.states_value[st]

	def reset(self):
		self.states = []

	def savePolicy(self):
		fw = open('policy_' + str(self.name), 'wb')
		pickle.dump(self.states_value, fw)
		fw.close()

	def loadPolicy(self, file):
		fr = open(file, 'rb')
		self.states_value = pickle.load(fr)
		fr.close()

