

class player:

	def __init__(self, number):
		self.player_number = number

	def move(self, board, move):
		board.apply_unitary(self.strategy(board, move))
		board.set_move(move)

	def strategy(self, board, move):
		#strategy for getting unitary U

		return U
