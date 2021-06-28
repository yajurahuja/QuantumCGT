from player import *
from game import *
import numpy as np
import sys

if __name__ == '__main__':
	np.set_printoptions(precision=2, threshold = sys.maxsize)
	size  = 3
	winp = 3
	turn = 1
	a = game(size, winp, turn)
	a.setup()
	a.play()
