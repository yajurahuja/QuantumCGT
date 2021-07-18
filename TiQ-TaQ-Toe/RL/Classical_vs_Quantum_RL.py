import numpy as np
from scipy import sparse


import random
from collections import Counter
import functools
import operator
import pickle

from qiskit import QuantumCircuit, QuantumRegister, execute
from qiskit import BasicAer

BOARD_ROWS = 3
BOARD_COLS = 3


class Game:
	def init(self, player1, player2):
		self.p1 = player1
		self.p2 = player2
		self.gameEnd = False
		self.turn = 1
		self.move = 0

	def initial_board():
		"""This is the initial board with amplitude 1 and 0s in all the places"""
		return [[1,'000000000']]

	def avaialable_positions(self, board, player):
		"""Given a board and a players whose turn it is, this method returns a set of 
		all positions on the board that player can make on the board"""
		positions = []
		for i in range(BOARD_ROWS):
			for j in range(BOARD_COLS):
				if board[(3 * i) + j] = '0':
				positions.append((i,j))
		return positions

	def getReward(self):
		"""After a game is finished, this method feeds the appropriate reward to the players"""
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
		"""Resets all members of the game after each time it has been played"""
		self.board = None
		self.board = None
		self.gameEnd = False
		self.turn = 0

	def winner(one_board):
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

	def play(self, rounds = 100):
	""" The user enters the number of rounds and the game is played than many number of times"""
		for i in range(rounds):
			if i % 100 == 0:
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
				actions, amps = player.chooseAction(positions, self.board, (self.turn))
				self.move(actions, amps)
				board_hash = self.getHash()
				player1.addState(board_hash)
				if(self.turn == 9)
					self.gameEnd = True
			win = self.winner()
			self.getReward()
			self.p1.reset()
			self.p2.reset()
			self.reset()
			self.turn = 0

	def move(self, actions, amps):
	new_board = []
	for n in range(len(self.gameboards)):
		i = self.gameboards[n][0]
		j = self.gameboards[n][1]
        zeros = [k for k in range(len(j)) if j.startswith('0', k)]
        if (len(zeros)>= 2):
            amp, chosen_zeros = amps[n], actions[n]
            new_amplitudes = [round((element*i).real,2)+round((element*i).imag,2)*1j for element in amp]
            new_positions = []
            for index in chosen_zeros:
                new_positions.append(j[:index] + player_number + j[index + 1:])
            current_board = [list(a) for a in zip(new_amplitudes, new_positions)]
            new_board.extend(current_board)
            #print('Initital:',i,j,'\nRandom Apms: ', amp, '\nRandom Positions: ',chosen_zeros,'\nNew Apms: ',new_amplitudes, '\nNew Positions: ',new_positions, '\nCurrent Board: ',current_board,'\n\n\n')
        elif (len(zeros)==1):
            for index in zeros:
                new_positions = j[:index] + player_number + j[index + 1:]
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

		hash = str(sparse.csr_matrix(normalised))
		return hash

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
		fullamps = [1, -1 , 1j, -1j]
		halfamps = [1/np.sqrt(2), -1/np.sqrt(2), 1j/np.sqrt(2), -1j/np.sqrt(2)]
		totalamps = [1, -1 , 1j, -1j, 1/np.sqrt(2), -1/np.sqrt(2), 1j/np.sqrt(2), -1j/np.sqrt(2)]
		if np.random.uniform(0, 1) <= self.exp_rate:
			idx = [np.random.choice(len(position), size = 2) for position in a]
			actions = [np.array(positions[i])[idx[i]] for i in range(len(positions))]
			amps = []
			for action in actions:
					amp1 = np.random.choice(totalamps)
					if amp1 in fullamps:
						amp2 = 0
					else:	
						amp2 = np.random.choice(halfamps)
					amps.append([amp1, amp2])
		else: 


		return actions, amps


	def chooseCAction2(self, positions, current_board, turn):
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

	def chooseCAction1(self, positions, current_board, turn):
		max_ = -9999
		action= None
		for i,j in positions:
			index = 3*i + j
			next_board = current_board.copy()
			next_board = next_board[:index] + str(turn) + next_board[index + 1:]
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
