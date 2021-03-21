from graphics import *
from qiskit import *
from sys import *
from player import *
from gamep import *


if __name__ == "__main__":
	size  = 3
	winp = 3
	turn = 1
	#boxSize = min(100,int(750/size))
	a = game(size, winp, turn)
	a.setup()
	for i in range(2):
		a.addplayer()
	a.play()


