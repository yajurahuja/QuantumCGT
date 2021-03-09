from graphics import *
from qiskit import *
from sys import*
from Tic_Tac_Toe import *

if __name__ == "__main__":
	size  = 3
	winp = 3
	turn = 1
	boxSize = min(100,int(750/size))
	a = game(size, winp, turn, boxSize)
	a.setup()
	a.main_window_g()
	while True:
		b = 1

