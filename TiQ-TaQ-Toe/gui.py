import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QStackedWidget,
    QListWidget,
    QGridLayout,
    QComboBox
)


class MainWindow(QWidget):
	def __init__(self, parent):
		super().__init__()
		self.setWindowTitle("Quantum Tic Tac Toe")
		self.data = None
		self.parent = parent
		self.a = None

		pagelayout = QVBoxLayout()

		heading = QHBoxLayout()
		lab = QLabel("Quantum Tic Tac Toe")
		font = lab.font()
		font.setPointSize(30)
		lab.setFont(font)
		lab.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		heading.addWidget(lab)
		pagelayout.addLayout(heading)


		p1layout = QHBoxLayout()
		p1label = QLabel("Player 1 Name: ")
		self.p1linput = QLineEdit()
		self.p1linput.setMaxLength(30)
		p1layout.addWidget(p1label)
		p1layout.addWidget(self.p1linput)
		pagelayout.addLayout(p1layout)

		p2layout = QHBoxLayout()
		p2label = QLabel("Player 2 Name: ")
		self.p2linput = QLineEdit()
		self.p2linput.setMaxLength(30)
		p2layout.addWidget(p2label)
		p2layout.addWidget(self.p2linput)
		pagelayout.addLayout(p2layout)


		buttonlayout = QHBoxLayout()
		button_play = QPushButton('Play')
		button_play.clicked.connect(self.play)
		buttonlayout.addWidget(button_play)
		pagelayout.addLayout(buttonlayout)
		self.setLayout(pagelayout)
		

	def play(self):
		print('play')
		self.parent.close()

		

	def return_data(self):
		return 	self.p1linput.text(), self.p2linput.text()
		
			

class TicTacToeWindow(QWidget):

	def __init__(self, parent, player_number, player_name, move, boardlist, current_board, amplist):
		super(TicTacToeWindow, self).__init__()
		self.setWindowTitle("Quantum Tic Tac Toe")
		self.parent = parent
		self.BoardPage= QVBoxLayout(self)
		self.boards  = []
		self.boxes = []
		self.amps = []
		self.boardlist = boardlist
		self.tttlayouts = []
		self.widgetm = []
		self.count = 0
		self.amplist = ['0', '1', '-1', 'i', '-i', '1/\u221A2', '-1/\u221A2', 'i/\u221A2', '-i/\u221A2']



		self.player_info = QHBoxLayout(self)
		self.BoardPage.addLayout(self.player_info)
		self.player_info.addWidget(QLabel("Player " + str(player_number)))
		self.player_info.addWidget(QLabel(player_name))
		self.player_info.addWidget(QLabel("Turn: " + str(move)))

		self.data = QHBoxLayout(self)
		self.BoardPage.addLayout(self.data)

		self.stack = QStackedWidget(self)
		self.leftlist = QListWidget()
		self.data.addWidget(self.leftlist)
		self.data.addWidget(self.stack)
		for i in range(len(boardlist)):
			self.leftlist.insertItem(i, boardlist[i])
			self.stackUI(boardlist[i], amplist[i], current_board)

		for i in range(len(boardlist)):
			for j in range(len(self.widgetm[i])):
				self.connect(i, j)


		buttonlayout = QHBoxLayout()
		button_play = QPushButton('Move')
		button_play.clicked.connect(self.move)
		buttonlayout.addWidget(button_play)
		self.BoardPage.addLayout(buttonlayout)
		self.setLayout(self.BoardPage)

		self.leftlist.currentRowChanged.connect(self.display)

	def connect(self, i, j):
		if type(self.widgetm[i][j]) == type(QComboBox()):
			self.widgetm[i][j].activated.connect(lambda : self.on_choice_change(i, j))
		
      
	def stackUI(self, board, amp, current_state):
		s = QWidget()
		
		vBox = QVBoxLayout(self)
		#l = current_state.find(amp)
		#amp = current_state[:l] +'<font color = black>'+current_state[l: l + len(amp)] + '</font>' + current_state[l + len(amp): ]
		amp = current_state
		state = QLabel(amp)
		Tictactoelayout = QGridLayout()
		wa = []
		for i in range(3):
			for j in range(3):
				index = (i*3) + j
				if board[index] == '0':
					ampcb = QComboBox()
					ampcb.addItems(self.amplist)
					Tictactoelayout.addWidget(ampcb, i, j) 
					wa.append(ampcb)
				else:
					a = QLabel(board[index])
					Tictactoelayout.addWidget(a, i, j)
					wa.append(0)
		self.widgetm.append(wa)
		vBox.addWidget(state)
		vBox.addLayout(Tictactoelayout)
		s.setLayout(vBox)
		self.tttlayouts.append(Tictactoelayout)
		self.stack.addWidget(s)

	def get_count(self, i):
		count = 0
		for j in range(len(self.widgetm[i])):
			if type(self.widgetm[i][j]) == type(QComboBox()) and self.widgetm[i][j].currentText() != '0':
				count = count + 1
		return count
	def on_choice_change(self, i, j):
		self.count = self.get_count(i)
		print(self.widgetm[i][j].currentText(), self.count)
		if type(self.widgetm[i][j]) == type(QComboBox()) and self.widgetm[i][j].currentText() in ['1', '-1', 'i', '-i']: 
			for k in range(len(self.widgetm[i])):
				if type(self.widgetm[i][k]) == type(QComboBox()) and self.widgetm[i][k].currentText() == '0':
					self.widgetm[i][k].setDisabled(True)
		elif type(self.widgetm[i][j]) == type(QComboBox()) and self.widgetm[i][j].currentText() in ['1/\u221A2', '-1/\u221A2', 'i/\u221A2', '-i/\u221A2']:
			print(self.widgetm[i][j].currentText(), 'F')
			if self.count == 1:
				for k in range(len(self.widgetm[i])):
					if type(self.widgetm[i][k]) == type(QComboBox()) and k != j:
						self.widgetm[i][k].clear()
						self.widgetm[i][k].addItems(['0', '1/\u221A2', '-1/\u221A2', 'i/\u221A2', '-i/\u221A2'])
						self.widgetm[i][k].setEnabled(True)
			elif self.count == 2:
				for k in range(len(self.widgetm[i])):
					if type(self.widgetm[i][k]) == type(QComboBox()) and self.widgetm[i][k].currentText() == '0':
						self.widgetm[i][k].setDisabled(True)
					if type(self.widgetm[i][k]) == type(QComboBox()) and self.widgetm[i][k].currentText() in ['1/\u221A2', '-1/\u221A2', 'i/\u221A2', '-i/\u221A2'] and k != j:
						for a in ['1', '-1', 'i', '-i']:
							self.widgetm[i][k].removeItem(self.widgetm[i][k].findText(a))

		elif type(self.widgetm[i][j]) == type(QComboBox()) and self.widgetm[i][j].currentText() == '0':
			if self.count == 1:
				for k in range(len(self.widgetm[i])):
					if type(self.widgetm[i][k]) == type(QComboBox()) and self.widgetm[i][k].currentText() not in ['1/\u221A2', '-1/\u221A2', 'i/\u221A2', '-i/\u221A2']:
						self.widgetm[i][k].clear()
						self.widgetm[i][k].addItems(['0', '1/\u221A2', '-1/\u221A2', 'i/\u221A2', '-i/\u221A2'])
						self.widgetm[i][k].setEnabled(True)
					elif type(self.widgetm[i][k]) == type(QComboBox()):
						self.widgetm[i][k].addItems(['1', '-1', 'i', '-i'])
			elif self.count == 0:
				for k in range(len(self.widgetm[i])):
					if type(self.widgetm[i][k]) == type(QComboBox()): 
						self.widgetm[i][k].clear()
						self.widgetm[i][k].addItems(self.amplist)
						self.widgetm[i][k].setEnabled(True)

	def move(self):
		print("move")
		self.get_data()
		self.parent.close()

	def display(self,i):
		self.stack.setCurrentIndex(i)

	def get_data(self):
		for i in range(len(self.boardlist)):
			for j in range(len(self.widgetm[i])):
						print(type(self.widgetm[i][j]))
						if type(self.widgetm[i][j]) == type(QComboBox()) and self.widgetm[i][j].currentText() != '0':
							print(self.widgetm[i][j].currentIndex())
							self.boards.append(self.boardlist[i])
							self.boxes.append(j)
							self.amps.append(self.widgetm[i][j].currentText())
		print("amps : ", self.amps)

	def return_data(self):
		return self.boards, self.boxes, self.amps

class WinnerWindow(QWidget):
	def __init__():
		super(WinnerWindow, self).__init__()
		self.setWindowTitle("Quantum Tic Tac Toe")
		




        




