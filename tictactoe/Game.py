from graphics import *
from qiskit import *
from sys import*

class game:
	def __init__(self, size, winp, turn, boxsize):
		self.boardsize = size
		self.win_parameter = winp
		self.turn = 1
		self.game_circuit = QuantumCircuit(boardsize ** 2, boardsize ** 2) # nXn size quantum circuit
		self.simulator = Aer.get_backend('qasm_simulator')
		self.boxsize = boxsize
		self.board = [[ 0 for i in range(size)] for j in range(size)] # board matrix
		self.turn = 1
		self.boxes = [[Rect(i*boxsize, j*boxsize, boxsize) for i in range(boardsize)]for j in range(boardsize)]
		self.moves = 0
		self.turn = 1			
		self.choice = ''
		self.points = []
		self.control_position = {}
		self.target_position = {}
		self.update = []

	def Rect(x,y, bs): # Create a rectanble box using diagonal points
		return Rectangle(Point(x,y+bs),Point(x+bs,y))

	def start_window_g(self):
		start_window = GraphWin("Welcome",600,600)
		start_window.setBackground('Black')
		qttt = Text(Point(300,50),"Quantum Tic-Tac-Toe")
		qttt.setSize(35)
		qttt.setTextColor(color_rgb(0,255,200))
		qttt.draw(start_window)
		welcome_msg ='Legal Moves:\n'\
		'- Classical Move: Collapses Box to black or white with equal probability\n'\
		'- Quantum Move: Entangles target box and control box. Reverses \ntarget box if control box collapses to black\n\n'\
		'Rules:\n'\
		'1) Initially all boxes are in Quantum State/superposition of \nblack and white\n'\
		'2) Only Classical move can collapses a quantum state to a \nclassical state\n'\
		'3) A  classical  move  can  only  be  applied  to  a  box  that\n  is in Quantum State '\
		'i.e. a classical  move cannot be apllied\n to the same box twice\n'\
		'4) The Quantum Move’s target box should be in a Classical \nState, and the control box should be in a Quantum State'
		start_window.setCoords(0,500,500,0)
		txt = Text(Point(250,200),welcome_msg)
		txt.setTextColor(color_rgb(0,255,200))
		txt.setSize(15)
		txt.draw(start_window)
		click = Rectangle(Point(200,375),Point(300,425))
		click.setFill('Orange')
		click.draw(start_window)
		click_txt = Text(Point(250,400),"Start")
		click_txt.setSize(20)
		click_txt.draw(start_window)
		while True:
			click_cord = start_window.getMouse()
			x = click_cord.getX()
			y = click_cord.getY()
			if 200<=x<=300 and 375<=y<=425:
				start_window.close()
				break

	def boxes_g(window)
		for row in self.boxes:
			for box in row:
				box.draw(window) 
				box.setFill("Grey")



	def main_window_g()
		main_win = GraphWin("Quantum Tic Tac Toe ",size * boxsize,size * boxsize+50)
		main_win.setCoords(0,size * boxsize+50,size * boxsize,0)
		boxes_g(main_win)

	def setup(self): # Setup the game circuit and initial display screen
		for i in range(boardsize ** 2):
			game_circuit.h(i)
		start_window_g() #Draw the window

	def boolp(x,y,n):
	if x >= size or y>=size or x<0 or y<0: 
		return False
	return n == board[x][y]

	def check_winner(): #Check if a  player is the winner
		for row in range(boardsize):
			for column in range(boardsize):
				box = board[row][column]
				if box == 0: continue

				#Check row
				check = True
				for i in range(winp):
					check = probe(row , column+i, box)
					if not check: break
					else: return box

				#Check column
				check = True
				for i in range(winp):
					check = boolp(row + i, column, box)
					if not check: break
					else: return box 
				
				#Check diagonal1
				check = True
				for i in range(winp):
					check = boolp(row + i, column + i, box)
					if not check: break
					else: return box

				#Check diagonal2
				check = True
				for i in range(winp):
					check = boolp(row - i , column + i, box)
					if not check: break
					else: return box
	return 0

	def interactive_play():
		col = ''
		while True: 
			if turn==1 : 
				col = 'White' 
			else:
				col = 'Black'
			turn_txt.undraw()
			turn_txt.setText('Turn : Player '+str(turn)+'('+col+')')
			turn_txt.draw(win)
			p = win.getMouse()
			y = int(p.getX() / boxSize) 
			x = int(p.getY() / boxSize) 
			if not (0<=x<size and 0<=y<size):
				continue
			ch = choice()
			message.undraw()
			if ch=='c':
				if l[x][y] > 0:
					message.setText('Illegal move')
					message.draw(win)
					continue
				coord = (x*size) + (y)
				err = cmove(x,y)
				modify_subscript()
				if err==1:
					continue
			elif ch=='q':
				if l[x][y] > 0:
					message.setText('Illegal move')
					message.draw(win)
					continue
				pp = win.getMouse()
				yy = int(pp.getX() / boxSize) 
				xx = int(pp.getY() / boxSize)
				coord_control = (x*size) + (y+1)
				coord_target = (xx*size)+ (yy+1)
				err = qmove(coord_control,coord_target)
				modify_subscript()
				if err==1:
					continue
			elif ch=='h':
				err = hmove(x,y)
				if err==1:
					continue

			turn = 3 - turn 
			status = check()
			if status == 1 : 
				print ("Player 1 wins")
				highlight("Dark Red")
				display_win(1)
				break
			if status == 2:
				print ("Player 2 wins")
				highlight("Dark Green")
				display_win(2)
				break
			moves += 1 

		if moves == size*size :
			print ("Draw match")
			for x in rec:
				for y in x:
					y.setFill("Blue")



	#should make a draw function for each of the graphic
	#move function
	#player class 
	# -player class will have different move functions 
	# we will call the move functions from inside the move function of the game class
	



	