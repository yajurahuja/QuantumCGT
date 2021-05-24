from player import*


class game:
	def __init__(self, size, winp, turn):
		self.board_size = size
		self.win_parameter = winp
		self.turn = 1
		self.board = None 
		self.move = 0	
		self.players = []

	def setup(self):
		self.board = Board(self.board_size)
		self.players.append(len(self.players) + 1)

	def addplayer(self):
		self.players.append(player(len(self.players) + 1))

	def play(self):
		for i in range(self.board_size**2):
			self.move()
		print(self.get_winner())

	def move(self):
		self.move += 1
		self.players[self.turn - 1].move(self.board, self.move)	


	def get_winner(self):
		collapsed_board = self.board.measure()



	





