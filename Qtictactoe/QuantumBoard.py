import cirq
import numpy as np
from gates import *

import time
start_time = time.time()

class Board():
	def __init__(self, size):
		self.qutrits = cirq.LineQid.range(size, dimension = 3) 
		self.circuit = cirq.Circuit()
		self.simulator = cirq.Simulator()
		self.move = 0

	def init(self):
		OpI = OperatorI(I)
		for i in range(len(self.qutrits)):
			self.circuit.append(OpI.on(self.qutrits[i]))
		self.get_current_state()

	def measure(self):
		for i in range(len(self.qutrits)):
			self.circuit.append(cirq.measure(self.qutrits[i]))
		print(self.circuit)
		result = self.simulator.run(self.circuit)
		collapsed = []
		for i in range(9):
			collapsed.append(result.measurements[str(i) + ' (d=3)'][0][0])
		return np.array(collapsed).reshape(3,3)

	def get_current_state(self):
		result = self.simulator.simulate(self.circuit)
		print(result)
		print('\n\n\n')


	def apply_unitary_9(self, player, unitary):
		app = Operator9(player, unitary)
		self.circuit.append(app.on(*self.qutrits))

	def apply_unitary_1(self, player, unitary, qindex):
		app = Operator1(player, unitary)
		self.circuit.append(app.on(self.qutrits[qindex]))
		#self.get_current_state()

	def apply_unitary_controlled(self, player, unitary, cindex, qindex):
		app = Operator1(player, unitary).controlled(control_values = [player],control_qid_shape = (3,))
		self.circuit.append(app.on(self.qutrits[cindex], self.qutrits[qindex]))
		#self.get_current_state()

	def apply_unitary_2(self, player, unitary, qi1, qi2 ):
		app = Operator1(player, unitary)
		self.circuit.append(app.on([self.qutrits[qi1], self.qutrits[qi2]]))

	def set_move(self, move):
		self.move = move

	def get_statevector(self):
		result = self.simulator.simulate(self.circuit)
		return result.dirac_notation(3)




class Operator9(cirq.Gate):
	def __init__(self, player, unitary):
		super(Operator9, self)
		self.player = player
		self.unitary = unitary

	def _qid_shape_(self):
		return (3, 3, 3, 3, 3, 3, 3, 3, 3)

	def _num_qubits_(self):
		return 9

	def _unitary_(self):
		return np.array(self.unitary)

	def _circuit_diagram_info_(self, args):
		return ["U_" + str(self.player)] * self.num_qubits() 

class Operator1(cirq.Gate):
	def __init__(self, player, unitary):
		super(Operator1, self)
		self.player = player
		self.unitary = unitary

	def _qid_shape_(self):
		return (3, )

	def _num_qubits_(self):
		return 1

	def _unitary_(self):
		return np.array(self.unitary)

	def _circuit_diagram_info_(self, args):
		return ["U_" + str(self.player)] * self.num_qubits()


class Operator2(cirq.Gate):
	def __init__(self, player, unitary):
		super(Operator1, self)
		self.player = player
		self.unitary = unitary

	def _qid_shape_(self):
		return (3, 3)

	def _num_qubits_(self):
		return 2

	def _unitary_(self):
		return np.array(self.unitary)

	def _circuit_diagram_info_(self, args):
		return ["U_" + str(self.player)] * self.num_qubits()


class OperatorI(cirq.Gate):
	def __init__(self, unitary):
		super(OperatorI, self)
		self.unitary = unitary

	def _qid_shape_(self):
		return (3, )

	def _num_qubits_(self):
		return 1

	def _unitary_(self):
		return np.array(self.unitary)

	def _circuit_diagram_info_(self, args):
		return "I"

# a = Board(9)
# a.init()
# a.apply_unitary_1(1, H['02'], 0)
# a.apply_unitary_1(1, X['01'],0)
# a.apply_unitary_controlled(1, X['01'], 0, 1)
# a.measure()




