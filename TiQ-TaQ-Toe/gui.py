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
    QComboBox,
    QScrollArea
)

def convertboard(board):
	new_board = ''
	for i in board:
		if i == '0':
			new_board = new_board + ' . '
		elif i == '1':
			new_board = new_board + 'X'
		elif i == '2':
			new_board = new_board + 'O'
	return new_board

def current_statestring(boardlist, amplist):
    string =''
    for i in range(len(boardlist)):
        if (i == (len(boardlist)-1)):           
            string = string + '('+str(round(amplist[i].real,2)) + '+' +  str(round(amplist[i].imag,2)) + 'i'+')' + '|'+ convertboard(boardlist[i]) + '>' 
        else:
            string = string + '('+str(round(amplist[i].real,2)) + '+' +  str(round(amplist[i].imag,2)) + 'i'+')' + '|'+ convertboard(boardlist[i]) + '>'+ ' + '
    return string


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
			amp = round(amplist[i].real ** 2, 2) + round(amplist[i].imag ** 2, 2)
			self.leftlist.insertItem(i, '|' + str(convertboard(boardlist[i])) + '>     Prob: ' + str(amp))          
			string = '('+str(round(amplist[i].real,2)) + '+' +  str(round(amplist[i].imag,2)) + 'i'+')' + '|'+ convertboard(boardlist[i]) + '>' 
			self.stackUI(boardlist[i], string, current_statestring(boardlist, amplist))

		for i in range(self.leftlist.count()):
			self.leftlist.item(i).setForeground(Qt.white)

		self.leftlist.setFixedSize(180, 200)

		for i in range(len(boardlist)):
			for j in range(len(self.widgetm[i])):
				self.connect(i, j)

		buttonlayout = QHBoxLayout()
		self.button_play = QPushButton('Move')
		self.button_play.setEnabled(False)
		self.button_play.clicked.connect(self.move)
		buttonlayout.addWidget(self.button_play)
		
		self.BoardPage.addLayout(buttonlayout)
		self.setLayout(self.BoardPage)
		self.leftlist.currentRowChanged.connect(self.display)

	def connect(self, i, j):
		if type(self.widgetm[i][j]) == type(QComboBox()):
			self.widgetm[i][j].activated.connect(lambda : self.on_choice_change(i, j))


	def stackUI(self, board, string, current_state):
		
		s = QWidget()
		vBox = QVBoxLayout(self)
		print("string", string)
		l = current_state.find(string)
		amp = '<font color = black>' + current_state[:l] + '</font>' +current_state[l: l + len(string)] + '<font color = black>'+ current_state[l + len(string): ] + '</font>' 
		print("string", amp)
		label = QLabel(amp)
		state =  QScrollArea()
		state.setWidget(label)
		state.setFixedSize(300, 50)
		state.setAlignment(Qt.AlignCenter)
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
					if board[index] == '1':
						a = QLabel('<font color = black size = \'10\'>' + 'X' + '</font>')
					else:
						a = QLabel('<font color = black size = \'10\'>' + 'O' + '</font>')
					a.setAlignment(Qt.AlignCenter)
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
		""" This function disables and enables the list elements depending of if the chosen amplitude squares 
		already add up to 1 or not"""
		self.count = self.get_count(i)
		print(self.widgetm[i][j].currentText(), self.count)

		if type(self.widgetm[i][j]) == type(QComboBox()) and self.widgetm[i][j].currentText() in ['1', '-1', 'i', '-i']: 
			for k in range(len(self.widgetm[i])):
				if type(self.widgetm[i][k]) == type(QComboBox()) and self.widgetm[i][k].currentText() == '0':
					self.widgetm[i][k].setDisabled(True)
			self.leftlist.item(i).setForeground(Qt.green)


		elif type(self.widgetm[i][j]) == type(QComboBox()) and self.widgetm[i][j].currentText() in ['1/\u221A2', '-1/\u221A2', 'i/\u221A2', '-i/\u221A2']:
			print(self.widgetm[i][j].currentText(), 'F')
			if self.count == 1:
				for k in range(len(self.widgetm[i])):
					if type(self.widgetm[i][k]) == type(QComboBox()) and k != j:
						self.widgetm[i][k].clear()
						self.widgetm[i][k].addItems(['0', '1/\u221A2', '-1/\u221A2', 'i/\u221A2', '-i/\u221A2'])
						self.widgetm[i][k].setEnabled(True)
				self.leftlist.item(i).setForeground(Qt.white)

			elif self.count == 2:
				for k in range(len(self.widgetm[i])):
					if type(self.widgetm[i][k]) == type(QComboBox()) and self.widgetm[i][k].currentText() == '0':
						self.widgetm[i][k].setDisabled(True)
					if type(self.widgetm[i][k]) == type(QComboBox()) and self.widgetm[i][k].currentText() in ['1/\u221A2', '-1/\u221A2', 'i/\u221A2', '-i/\u221A2'] and k != j:
						for a in ['1', '-1', 'i', '-i']:
							self.widgetm[i][k].removeItem(self.widgetm[i][k].findText(a))
				self.leftlist.item(i).setForeground(Qt.green)

		elif type(self.widgetm[i][j]) == type(QComboBox()) and self.widgetm[i][j].currentText() == '0':
			if self.count == 1:
				for k in range(len(self.widgetm[i])):
					if type(self.widgetm[i][k]) == type(QComboBox()) and self.widgetm[i][k].currentText() not in ['1/\u221A2', '-1/\u221A2', 'i/\u221A2', '-i/\u221A2']:
						self.widgetm[i][k].clear()
						self.widgetm[i][k].addItems(['0', '1/\u221A2', '-1/\u221A2', 'i/\u221A2', '-i/\u221A2'])
						self.widgetm[i][k].setEnabled(True)
					elif type(self.widgetm[i][k]) == type(QComboBox()):
						self.widgetm[i][k].addItems(['1', '-1', 'i', '-i'])
				self.leftlist.item(i).setForeground(Qt.white)
			elif self.count == 0:
				for k in range(len(self.widgetm[i])):
					if type(self.widgetm[i][k]) == type(QComboBox()): 
						self.widgetm[i][k].clear()
						self.widgetm[i][k].addItems(self.amplist)
						self.widgetm[i][k].setEnabled(True)
				self.leftlist.item(i).setForeground(Qt.white)
		flag = True
		for i in range(self.leftlist.count()):
			if str(self.leftlist.item(i).foreground().color().rgb()) == '4294967295':
				flag = False
		if not flag:
			self.button_play.setEnabled(False)
		else:
			self.button_play.setEnabled(True)





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
	def __init__(self, player_name, result):
		super(WinnerWindow, self).__init__()
		self.setWindowTitle("Quantum Tic Tac Toe")

		pagelayout = QVBoxLayout()
		Tictactoelayout = QGridLayout()
		for i in range(3):
			for j in range(3):
				index = (i*3) + j
				if result[index] == '1':
					a = QLabel('<font color = black size = \'10\'>' + 'X' + '</font>')
				elif result[index] == '2':
					a = QLabel('<font color = black size = \'10\'>' + 'O' + '</font>')
				a.setAlignment(Qt.AlignCenter)
				Tictactoelayout.addWidget(a, i, j)
		pagelayout.addLayout(Tictactoelayout)
		Winnerlayout = QHBoxLayout()
		a = QLabel('<font color = black size = \'10\'>' + player_name + '</font>')
		a.setAlignment(Qt.AlignCenter)
		Winnerlayout.addWidget(a)
		pagelayout.addLayout(Winnerlayout)
		self.setLayout(pagelayout)



		




        




