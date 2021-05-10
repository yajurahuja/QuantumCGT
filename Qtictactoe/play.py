from player import *
from game import *
import numpy as np

if __name__ == '__main__':
	np.set_printoptions(precision=2)
	size  = 3
	winp = 3
	turn = 1
	a = game(size, winp, turn)
	a.setup()
	for i in range(2):
		a.addplayer()
	a.play()