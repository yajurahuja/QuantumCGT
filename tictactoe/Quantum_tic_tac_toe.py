from graphics import *
from qiskit import *
from sys import*

size = winp = 0
while True:
	size = int(input("Enter the size of the tic tac toe board you wanna play: "))
	winp = int(input("Enter the winning parameter k: "))
	if winp > size : 
		print ("size of board cannot be less than winning parameter, try again.")
		continue
	break

boxSize = min(100,int(750/size))
circuit=QuantumCircuit(size*size,size*size)

def setup(): #Initial Window
	for i in range(size*size):
		circuit.h(i)
	start_window = GraphWin("Welcome",600,600)
	start_window.setBackground('Black')
	quantum = Text(Point(300,50),"Quantum Tic-Tac-Toe")
	quantum.setSize(35)
	quantum.setTextColor(color_rgb(0,255,200))
	quantum.draw(start_window)
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
		click_coord = start_window.getMouse()
		x = click_coord.getX()
		y = click_coord.getY()
		if 200<=x<=300 and 375<=y<=425:
			start_window.close()
			break


setup()

moves = 0
turn = 1			
ch = ''
points = []
control_pos = {}
target_pos = {}
update = []
box_text = []

for i in range(size):
	temp = []
	for j in range(size):
		txt = Text(Point(j*boxSize+50,i*boxSize+10),'')
		txt.setTextColor("Green")
		temp.append(txt)
	box_text.append(temp)

l = [[0 for i in range(size)]for j in range(size)] #Board Final Values

def Rect(x,y):
	return Rectangle(Point(x,y+boxSize),Point(x+boxSize,y))

rec = [[Rect(i*boxSize,j*boxSize) for i in range(size)]for j in range(size)] #Box Positions to draw

win = GraphWin("Quantum Tic Tac Toe ",size * boxSize,size * boxSize+50) # Main Window
win.setCoords(0,size * boxSize+50,size * boxSize,0)


for x in rec: 
	for y in x:
		y.draw(win)
for x in rec: 
	for y in x:
		y.setFill('Gray')
		
def probe(x,y,n): #Check if valid index
	if x >= size or y>=size or x<0 or y<0: 
		return False
	return n == l[x][y]
	
def highlight(color): # setting final value on board if a suite is won and the colour the boxes
	color = "Dark Green"
	for x in range(size):
		for y in range(size):
			n = l[x][y]
			if n == 0 : continue
			flag = True
			for i in range(winp):
				flag = probe(x+i,y,n)
				if flag == False:
					break
			if flag : 
				for i in range(winp):
					rec[x+i][y].setFill(color)
				return 0
		
			flag = True
			for i in range(winp):
				flag = probe(x+i,y+i,n)
				if flag == False:
					break
			if flag : 
				for i in range(winp):
					rec[x+i][y+i].setFill(color)
				return 0
			
			flag = True
			for i in range(winp):
				flag = probe(x,y+i,n)
				if flag == False:
					break
			if flag : 
				for i in range(winp):
					rec[x][y+i].setFill(color)
				return 0
				
			flag = True
			for i in range(winp):
				flag = probe(x-i,y+i,n)
				if flag == False:
					break
			if flag : 
				for i in range(winp):
					rec[x-i][y+i].setFill(color)
				return 0
	return 0

	
def check():   #Check if a suite has been won
	for x in range(size):
		for y in range(size):
			n = l[x][y]
			if n == 0 : continue
			flag = True
			for i in range(winp):
				flag = probe(x+i,y,n)
				if flag == False:
					break
			if flag : return n
			
			flag = True
			for i in range(winp):
				flag = probe(x+i,y+i,n)
				if flag == False:
					break
			if flag : return n
			
			flag = True
			for i in range(winp):
				flag = probe(x,y+i,n)
				if flag == False:
					break
			if flag : return n

			flag = True
			for i in range(winp):
				flag = probe(x-i,y+i,n)
				if flag == False:
					break
			if flag : return n
	return 0

def modify(pos): #Colouring a box after measuring 
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

def modify_subscript(): #Reset a coloured box
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


def cmove(x,y): #Classical move
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


def qmove(control_bit,target_bit): #Quantum move
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

def hmove(x,y): #Reset move
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


def choice(): #Choice made by user
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


def display_win(player): 
	winning = GraphWin("Finish",250,250)
	winning.setBackground('Black')
	msg = Text(Point(125,125),"Player " + str(player) + " wins\nClick to continue")
	msg.setTextColor("Orange")
	msg.setSize(25)
	msg.draw(winning)
	winning.getMouse()

modify_subscript()
turn_txt = Text(Point(boxSize*(size/2),boxSize*size+15),'')
turn_txt.setSize(15)
message = Text(Point(boxSize*(size/2),boxSize*size+35),'')
message.setSize(15)
message.draw(win)
turn_txt.draw(win)
col = ''

while True : #Game Loop
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

