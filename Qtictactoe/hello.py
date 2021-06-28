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
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Quantum Tic Tac Toe")

		pagelayout = QVBoxLayout()

		heading = QHBoxLayout()
		lab = QLabel("Quantum Tic Tac Toe\n")
		font = lab.font()
		font.setPointSize(50)
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
		self.close()

		

			

class TicTacToeWindow(QWidget):

	def __init__(self, boardlist, current_board, amplist):
		super(TicTacToeWindow, self).__init__()
		self.setWindowTitle("Quantum Tic Tac Toe")
		self.BoardPage= QVBoxLayout(self)
		self.data = QHBoxLayout(self)
		self.BoardPage.addLayout(self.data)

		self.stack = QStackedWidget(self)
		self.leftlist = QListWidget()
		self.data.addWidget(self.leftlist)
		self.data.addWidget(self.stack)
		for i in range(len(boardlist)):
			self.leftlist.insertItem(i, boardlist[i])
			self.stackUI(boardlist[i], amplist[i])

		buttonlayout = QHBoxLayout()
		button_play = QPushButton('Move')
		button_play.clicked.connect(self.move)
		buttonlayout.addWidget(button_play)
		self.BoardPage.addLayout(buttonlayout)
		self.setLayout(self.BoardPage)

		self.leftlist.currentRowChanged.connect(self.display)

      
	def stackUI(self, board, amp):
		s = QWidget()
		amplist = ['0', '1', '-1', 'i', '-i', '1/np.sqrt(2)', '-1/np.sqrt(2)', 'i/np.sqrt(2)', '-i/np.sqrt(2)']
		vBox = QVBoxLayout(self)
		amplitude = QLabel(amp)
		Tictactoelayout = QGridLayout()
		for i in range(3):
			for j in range(3):
				index = (i*3) + j
				if board[index] == '0':
					ampcb = QComboBox()
					ampcb.addItems(amplist)
					Tictactoelayout.addWidget(ampcb, i, j) 
				else:
					Tictactoelayout.addWidget(QLabel(board[index]), i, j)
		vBox.addWidget(amplitude)
		vBox.addLayout(Tictactoelayout)
		s.setLayout(vBox)
		self.stack.addWidget(s)

	def move(self):
		print("move")


	def display(self,i):
		self.stack.setCurrentIndex(i)


        


app = QApplication(sys.argv)

window = MainWindow()
widget = QStackedWidget()
widget.setWindowTitle("Quantum TicTacToe")
widget.show()
widget.addWidget(window)
app.exec()
second = TicTacToeWindow(['000000000', '000000001'], '-1', ['1', '1'])
widget.addWidget(second)
widget.setCurrentIndex(widget.currentIndex() + 1)
widget.show()
app.exec()





