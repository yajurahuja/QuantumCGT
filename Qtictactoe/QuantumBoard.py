import cirq
import numpy as np

import time
start_time = time.time()




X_1 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
X_2 = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])


class Board():
	def __init__(self, size):
		self.qutrits = cirq.LineQid.range(size, dimension = 3) 
		self.circuit = cirq.Circuit()
		self.simulator = cirq.Simulator()
		self.move = 0

	def measure(self):
		for i in range(len(self.qutrits)):
			self.circuit.append(cirq.measure(self.qutrits[i]))
		print(self.circuit)
		print(self.simulator.run(self.circuit))

	def apply_unitary_9(self, player, unitary):
		test = Operator9(player, unitary)
		self.circuit.append(test.on(*self.qutrits))

	def apply_unitary_1(self, player, unitary, qindex):
		test = Operator1(player, unitary)
		self.circuit.append(test.on(self.qutrits[qindex]))

	def set_move(self, move):
		self.move = move



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


a = Board(9)
a.apply_unitary_1(1, X_1, 0)
print("--- %s seconds ---" % (time.time() - start_time))

a.apply_unitary_9(2, np.kron(np.eye(3**8), X_2))
a.measure()

print("--- %s seconds ---" % (time.time() - start_time))



