from player import*
from QuantumBoard import*
from gui import *
import sys



class game:
	def __init__(self, size, winp, turn):
		self.board_size = size
		self.win_parameter = winp
		self.turn = 1
		self.board = None 
		self.moves = 0	
		self.players = []
		self.app = QApplication(sys.argv)
		self.widgit = None


	def setup(self):
		self.board = Board(self.board_size**2)
		self.board.init()
		self.board.current_board = self.board.get_statevector()
		self.setupGui()

	def setupGui(self):
		self.widget = QStackedWidget()
		self.widget.setWindowTitle("Quantum TicTacToe")
		window = MainWindow(self.widget)
		self.widget.addWidget(window)
		self.widget.show()
		self.app.exec()


	def addplayers(self):
		p1, p2 = self.widget.currentWidget().return_data()
		self.players.append(player(1, p1))
		self.players.append(player(2, p2))

	def play(self):
		self.addplayers()
		for i in range(self.board_size**2):
			self.move()
		print("Winner: ", self.get_winner())

	def move(self):
		self.moves += 1
		self.players[self.turn - 1].move(self.board, self.moves, self.board.current_board, self.widget, self.app)
		#self.players[self.turn - 1].move_9(self.board, self.moves)
		self.turn = 3 - self.turn
		self.board.current_board = self.board.get_statevector()
		#print(self.board.current_board)
		#print('\n\n\n')
				

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
			




