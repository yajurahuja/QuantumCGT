from graphics import *
from qiskit import *
from sys import*


class player:
	
	def __init__(self, number):
		self.player_number = number

class cplayer(player):

	#def __init__(self):
	def cmove(row, column, size, sim):
		index = (row * size) + (column + 1)
		circuit.measure(index - 1, bize**2 - index)
		result = execute(circuit, backend=sim, shots=1).result()
		circuit_array = list(result.get_counts(circuit).keys())[0]
		error=0
		if pos not in points:
			if circuit_array[pos-1]=='1':
				circuit.reset(pos-1)
				circuit.x(pos-1)
				circuit.measure(pos-1,size*size-pos)
			else:
				circuit.reset(pos-1)
				circuit.measure(pos-1,size*size-pos)

			if pos in control_pos.keys():
				for target in control_pos[pos]:
					circuit.cx(pos-1,target-1)
				for target in control_pos[pos]:
					circuit.measure(target-1,size*size-target)
		else:
			global message
			message.setText('Illegal move')
			message.draw(win)
			error=1
		points.append(pos)
		modify(pos)
		return error




class qplayer(cplayer):

	def qmove(control_bit,target_bit, points):
		if target_bit in points and control_bit not in points:
			
			if target_bit in target_pos.keys():
				target_pos[target_bit].append(control_bit)
			else:
				target_pos[target_bit] = [control_bit]

			if control_bit in control_pos.keys():
				control_pos[control_bit].append(target_bit)
			else:
				control_pos[control_bit] = [target_bit]
			print(control_bit,'-',target_bit,' ',"entangled")
			return 0
		else :
			global message
			message.setText('Illegal move')
			message.draw(win)
			return 1

	def hmove(row, column, size, target_positon):
		index = (row * size) + (column + 1)
		if index in points and index not in target_position.keys():
			circuit.reset(index-1)
			circuit.h(index-1)
			rec[x][y].setFill('Gray')
			points.remove(pos)
			l[x][y] = 0
			return 0

		else:
			global message
			message.setText('Illegal move')
			message.draw(win)
			return 1
