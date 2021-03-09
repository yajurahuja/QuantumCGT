from graphics import *
from qiskit import *
from sys import*

class game:
	def __init__(self, size, winp, turn, boxsize):
		self.boardsize = size
		self.win_parameter = winp
		self.turn = 1
		self.game_circuit = QuantumCircuit(size ** 2, size ** 2) # nXn size quantum circuit
		self.simulator = Aer.get_backend('qasm_simulator')
		self.boxsize = boxsize
		self.board = [[ 0 for i in range(size)] for j in range(size)] # board matrix
		self.turn = 1
		self.boxes = [[ Rectangle(Point(i*boxsize, (j+1)*boxsize),Point((i+1)*boxsize, j*boxsize)) for i in range(size)]for j in range(size)]
		self.moves = 0
		self.turn = 1			
		self.choice = ''
		self.points = []
		self.control_position = {}
		self.target_position = {}
		self.update = []

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

	def boxes_g(self, window):
		for row in self.boxes:
			for box in row:
				box.draw(window) 
				box.setFill("Grey")

	def main_window_g(self):
		main_win = GraphWin("Quantum Tic Tac Toe ", self.boardsize * self.boxsize, (self.boardsize * self.boxsize)+50)
		main_win.setCoords(0, (self.boardsize * self.boxsize)+50, self.boardsize * self.boxsize,0)
		self.boxes_g(main_win)


	def setup(self): # Setup the game circuit and initial display screen
		for i in range(self.boardsize * self.boardsize):
			self.game_circuit.h(i)
		self.start_window_g() #Draw the window

			
	def probe(self, x, y, n):
		if x >= self.boardsize or y >= self.baordsize or x < 0 or y < 0: 
			return False
		return n == self.board[x][y]
		
	def highlight(self, color):
		color = "Dark Green"
		for x in range(self.boardsize):
			for y in range(self.boardsize):
				n = self.board[x][y]
				if n == 0 : continue
				flag = True
				for i in range(self.winp):
					flag = probe(x+i,y,n)
					if flag == False:
						break
				if flag : 
					for i in range(self.winp):
						self.boxes[x+i][y].setFill(color)
					return 0
			
				flag = True
				for i in range(self.winp):
					flag = probe(x+i,y+i,n)
					if flag == False:
						break
				if flag : 
					for i in range(self.winp):
						self.boxes[x+i][y+i].setFill(color)
					return 0
				
				flag = True
				for i in range(self.winp):
					flag = probe(x,y+i,n)
					if flag == False:
						break
				if flag : 
					for i in range(self.winp):
						self.boxes[x][y+i].setFill(color)
					return 0
					
				flag = True
				for i in range(self.winp):
					flag = probe(x-i,y+i,n)
					if flag == False:
						break
				if flag : 
					for i in range(self.winp):
						self.boxes[x-i][y+i].setFill(color)
					return 0
		return 0

		
	def check():
		for x in range(self.boardsize):
			for y in range(self.boardsize):
				n = self.board[x][y]
				if n == 0 : continue
				flag = True
				for i in range(self.winp):
					flag = probe(x+i,y,n)
					if flag == False:
						break
				if flag : return n
				
				flag = True
				for i in range(self.winp):
					flag = probe(x+i,y+i,n)
					if flag == False:
						break
				if flag : return n
				
				flag = True
				for i in range(self.winp):
					flag = probe(x,y+i,n)
					if flag == False:
						break
				if flag : return n

				flag = True
				for i in range(self.winp):
					flag = probe(x-i,y+i,n)
					if flag == False:
						break
				if flag : return n
		return 0

	def modify(pos):
		simulator=Aer.get_backend('qasm_simulator')
		result=execute(circuit,backend=simulator,shots=1).result()
		tem=result.get_counts(circuit).keys()
		tem=list(tem)
		circuit_array=tem[0]
		tem_pos=0
		for i in points:
			xx = int((i-1)/size)
			yy = int((i-1)%size)
			print(xx,yy)
			if (circuit_array[i-1]=='0' and l[xx][yy]!=1):
				l[xx][yy] = 1
				color = "white"
				rec[xx][yy].setFill(color)
			elif (circuit_array[i-1]=='1' and l[xx][yy]!=2):
				l[xx][yy] = 2
				color = "black"
				rec[xx][yy].setFill(color)
		if pos in control_pos.keys():
			for target in control_pos[pos]:
				target_pos[target].remove(pos)
			del control_pos[pos]

	def modify_subscript():
		for i in range(size*size):
			xx = int((i)/size)
			yy = int((i)%size)

			if i+1 in control_pos.keys():
				box_text[xx][yy].undraw()
				box_text[xx][yy].setText(str(control_pos[i+1]))
				box_text[xx][yy].draw(win)
			elif i+1 in target_pos.keys():
				box_text[xx][yy].undraw()
				box_text[xx][yy].setText(str(target_pos[i+1]))
				box_text[xx][yy].draw(win)
			else:
				box_text[xx][yy].undraw()
				box_text[xx][yy].setText(str(list()))
				box_text[xx][yy].draw(win)


	def cmove(x,y):
		pos = (x*size) + (y+1)
		circuit.measure(pos-1,size*size-pos)
		simulator=Aer.get_backend('qasm_simulator')
		result=execute(circuit,backend=simulator,shots=1).result()
		tem=result.get_counts(circuit).keys()
		tem = list(tem)
		circuit_array = tem[0]
		err=0
		if pos not in points:
			if circuit_array[pos-1]=='1':
				circuit.reset(pos-1)
				circuit.x(pos-1)
				circuit.measure(pos-1,size*size-pos)
			else:
				circuit.reset(pos-1)
				circuit.measure(pos-1,size*size-pos)

			if pos in control_pos.keys():
				for target in control_pos[pos]:
					circuit.cx(pos-1,target-1)
				for target in control_pos[pos]:
					circuit.measure(target-1,size*size-target)
		else:
			global message
			message.setText('Illegal move')
			message.draw(win)
			err=1
		points.append(pos)
		modify(pos)
		return err


	def qmove(control_bit,target_bit):
		if target_bit in points and control_bit not in points:
			
			if target_bit in target_pos.keys():
				target_pos[target_bit].append(control_bit)
			else:
				target_pos[target_bit] = [control_bit]

			if control_bit in control_pos.keys():
				control_pos[control_bit].append(target_bit)
			else:
				control_pos[control_bit] = [target_bit]
			print(control_bit,'-',target_bit,' ',"entangled")
			return 0
		else :
			global message
			message.setText('Illegal move')
			message.draw(win)
			return 1

	def hmove(x,y):
		pos = (x*size) + (y+1)
		if pos in points and pos not in target_pos.keys():
			circuit.reset(pos-1)
			circuit.h(pos-1)
			rec[x][y].setFill('Gray')
			points.remove(pos)
			l[x][y] = 0
			return 0

		else:
			global message
			message.setText('Illegal move')
			message.draw(win)
			return 1


	def choice():
		bsize = 100
		s = 2
		rec = [[Rect(i*bsize,50)] for i in range(s)]
		hchoice = Rect(50,150)
		win_choice = GraphWin("Choose Move",(s) * bsize,(s) * bsize+100)
		win_choice.setCoords(0,(s) * bsize+100,(s) * bsize,0)
		for x in rec: 
			for y in x:
				y.draw(win_choice)
		hchoice.draw(win_choice)

		txt = Text(Point(50,100),"Q move")
		txt.draw(win_choice)
		txt = Text(Point(150,100),"C move")
		txt.draw(win_choice)
		txt = Text(Point(100,200),"H move")
		txt.draw(win_choice)

		f = 1
		while f==1:
			p = win_choice.getMouse()
			y = int(p.getX() / boxSize)
			x = p.getY()-50
			xx = int(x / boxSize)
			
			if y==0 and xx==0 and x>=0:
				win_choice.close()
				return 'q'
			        
			elif y==1 and xx==0 and x>=0:
				win_choice.close()
				return 'c'

			elif 50<= p.getX() <=150 and 150<= p.getY() <=250:
				win_choice.close()
				return 'h'
