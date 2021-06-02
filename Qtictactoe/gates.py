import numpy as np

X = {'01': np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]]), 
	 '02': np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]]), 
	 '12': np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])}

H = {'01': (1 / np.sqrt(2)) * np.array([[1, 1, 0], [1, -1, 0], [0, 0, np.sqrt(2)]]), 
	 '02': (1 / np.sqrt(2)) * np.array([[1, 0, 1], [0, np.sqrt(2) , 0], [1, 0, -1]]), 
	 '12': (1 / np.sqrt(2)) * np.array([[np.sqrt(2), 0, 0], [0, 1, 1], [0, 1, -1]])}
	 
I = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

def R_y(rad, values):
	rad = rad /2
	Ry = {'01': np.round(np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0, 0, 1]]), decimals = 5), 
	 	  '02': np.round(np.array([[np.cos(rad), 0, -np.sin(rad)], [0, 1, 0], [np.sin(rad), 0, np.cos(rad)]]), decimals = 5), 
	 	  '12': np.round(np.array([[1, 0, 0], [0, np.cos(rad), -np.sin(rad)], [0, np.sin(rad), np.cos(rad)]]), decimals = 5)}

	return Ry[values]
