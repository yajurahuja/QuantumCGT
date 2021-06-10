from player import*
from QuantumBoard import*



class game:
	def __init__(self, size, winp, turn):
		self.board_size = size
		self.win_parameter = winp
		self.turn = 1
		self.board = None 
		self.moves = 0	
		self.players = []


	def setup(self):
		self.board = Board(self.board_size**2)
		self.board.init()


	def addplayer(self):
		self.players.append(player(len(self.players) + 1))

	def play(self):
		for i in range(self.board_size**2):
			self.move()
		print("Winner: ", self.get_winner())

	def move(self):
		self.moves += 1
		self.players[self.turn - 1].move_9(self.board, self.moves)
		self.turn = 3 - self.turn
		print(self.board.get_statevector())
		print('\n\n\n')
				

	def get_winner(self):
		collapsed_board = self.board.measure()
		print(collapsed_board)
		p1 = 0
		p2 = 0
		d1 = []
		d2 = []
		#row_column check
		for i in range(len(collapsed_board)):
			p1, p2 = get_suite(collapsed_board[i ,:], p1, p2) #row
			p1, p2 = get_suite(collapsed_board[:,i], p1, p2) #column
		#diag check
		p1, p2 = get_suite(collapsed_board.diagonal() ,p1, p2)
		p1, p2 = get_suite(np.fliplr(collapsed_board).diagonal(), p1, p2)
		print(p1, p2)
		if(p1 > p2):
			return 1
		elif(p2 > p1):
			return 2
		else:
			return 0


def get_suite( arr, p1, p2):
	arr = np.array(arr)
	result = np.all(arr == arr[0])
	if result:
		if(arr[0] == 1):
			p1 += 1
		elif(arr[0] == 2):
			p2 += 1
	return p1, p2
			




