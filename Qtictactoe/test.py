import numpy as np

class Qutrit:
	def __init__(self):
		self.vec = self.init()

	def init(self):
		qutrit_array = np.zeros(3, dtype = np.cdouble)
		qutrit_array[0] = 1
		return qutrit_array

	def update(self, vector):
		self.vec = np.array(vector)

	@staticmethod
	def tensor(qutrit_array):
		tensor_product = np.array([1.0])
		for qutrit in qutrit_array:
			tensor_product = np.kron(tensor_product, qutrit.vec)
		return tensor_product

	@staticmethod
	def apply(gate_array, qutrit_array):
		if len(gate_array) == len(qutrit_array):
			return np.dot(Gate.tensor(gate_array), Qutrit.tensor(qutrit_array))
		else:
			return None

class Gate:
	def __init__(self, gate_matrix):
		self.mat = np.matrix(gate_matrix)

	@staticmethod
	def tensor(gate_array):
		tensor_product = np.matrix([1.0])
		for gate in gate_array:
			tensor_product = np.kron(tensor_product, gate.mat)
		return tensor_product


b = Gate([[1, 1, 0], [1, 0, 0], [0, 0, 1]])
c = Qutrit()

ab = Qutrit.apply([b], [c])
print(ab)