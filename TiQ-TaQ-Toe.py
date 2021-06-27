import numpy as np
from itertools import product
import random
from collections import Counter
import functools
import operator

def initial_board():
  '''This is the initial board with amplitude 1 and 0s in all the places'''
  
    initial_board = [[1,'000000000']]
    return initial_board
    
def amplitudes():
  '''This returns a list of valid combinations of amplitudes 
      Eg. [[1,0],[0,1],[-1,0].....]''''
  
    all_amplitudes = [0, 1, -1 , 1j, -1j, 1/np.sqrt(2), -1/np.sqrt(2), 1j/np.sqrt(2), -1j/np.sqrt(2)]

    perm = list(product(all_amplitudes,repeat=2))
        
    amplitudes = []
    for i in perm:
        if(round((abs(i[0])**2 + abs(i[1]**2)),1)==1 or (abs(i[0])**2 + abs(i[1]**2))==1):
            amplitudes.append(list(i))
    return amplitudes
    

def action(one_board):
  '''This funnction returns the randomly chosen amplitudes and positions that is to be replaced.
      Eg. amp = [0,1], chosen_zeros = [3,7]
      
      one_board: list (It is a single board from all the possible boards in the list of boards)
                 Eg. [1,'121221112']'''
  
    amplitude_list = amplitudes()
    amp = random.choice(amplitude_list)
    zeros = [k for k in range(len(one_board)) if one_board.startswith('0', k)]
    #print(zeros)
    if (len(zeros)>= 2):
        chosen_zeros = random.sample(set(zeros), 2)
        return amp, chosen_zeros  #This returns the amplitudes and positions chosen
    elif (len(zeros)==1):
        chosen_zeros = random.sample(set(zeros), 1)
        return chosen_zeros       #This returns only the positions since in the last move amplitudes are not important
    else:
        return 'Invalid'
        
       

def move(board,player_number):
  '''This updates the provided board to the new board/game position and resturns the nested list of the new_board
    
    board: nested list (It is the current game position)
            Eg. [[1/sqrt(2),'121221112'],[1/sqrt(2),'111221212']]
    player_number: char (It is the number/char of the player)'''
  
    new_board = []
    for i,j in board:
        zeros = [k for k in range(len(j)) if j.startswith('0', k)]
        if (len(zeros)>= 2):
            amp, chosen_zeros = action(j)
            new_amplitudes = [round((element*i).real,2)+round((element*i).imag,2)*1j for element in amp]
            new_positions = []
            for index in chosen_zeros:
                new_positions.append(j[:index] + player_number + j[index + 1:])
            current_board = [list(a) for a in zip(new_amplitudes, new_positions)]
            new_board.extend(current_board)
            #print('Initital:',i,j,'\nRandom Apms: ', amp, '\nRandom Positions: ',chosen_zeros,'\nNew Apms: ',new_amplitudes, '\nNew Positions: ',new_positions, '\nCurrent Board: ',current_board,'\n\n\n')
        elif (len(zeros)==1):
            for index in zeros:
                new_positions = j[:index] + player_number + j[index + 1:]
            current_board = [[i, new_positions]]
            new_board.extend(current_board)
        else:
            new_board = board 
    
    #Combining same boards
    flat = functools.reduce(operator.iconcat, new_board, [])
    duplicate_items = ([item for item, count in Counter(flat).items() if (count > 1 and type(item)==str)])
    concatenated_list = []
    all_indexes = []
    for i in duplicate_items:
        indexes = []
        for j in new_board:
            if (i==j[1]):
                indexes.append(new_board.index(j))
                all_indexes.append(new_board.index(j))
        total_amp = 0
        for k in indexes:
            total_amp += new_board[k][0]
        combined_ele = [total_amp,i]
        concatenated_list.append(combined_ele)
    for ele in sorted(all_indexes, reverse = True): 
            del new_board[ele]
    new_board.extend(concatenated_list)
    
    #Removing boards with amplitude 0
    unwanted = []
    for i in new_board:
        if(i[0]==False):
            unwanted.append(new_board.index(i))
    for ele in sorted(unwanted, reverse = True): 
        del new_board[ele]
                    
    return new_board


def status(one_board,player_number):
  ''' This function returns a 1 if that particular board is a winning board for the player, -1 if it is winning board for opponent and 0 if it's draw'''
    
    zeros = [k for k in range(len(one_board)) if one_board.startswith('0', k)]
    opponent_number = '2' if player_number=='1' else '1'
    
    diags = [[one_board[0],one_board[4],one_board[8]],[one_board[2],one_board[4],one_board[6]]]
    rows = [[one_board[0],one_board[1],one_board[2]],[one_board[3],one_board[4],one_board[5]],[one_board[6],one_board[7],one_board[8]]]
    cols =[[one_board[0],one_board[3],one_board[6]],[one_board[1],one_board[4],one_board[7]],[one_board[2],one_board[5],one_board[8]]]
    combined = diags + rows + cols
    
    if(len(zeros)==0):
        if(any(i.count(player_number)==3 for i in combined) and all(i.count(opponent_number)!=3 for i in combined)): #win condition
            return 1
        elif (any(i.count(opponent_number)==3 for i in combined) and all(i.count(player_number)!=3 for i in combined)): #lose condition
            return -1
        else:                                                                                                           #draw
            return 0

def reward(board, player_number):
  '''This returns the reward of the player entered'''
  
    sum_rewards = 0
    for i,j in board:
        #sum_rewards += round((abs(i**2))*status(j,player_number)*100,2)
        result = status(j,player_number)
        if(result==1):
            sum_rewards += (abs(i**2))*status(j,player_number)*100
    sum_rewards = round(sum_rewards,2)
    return sum_rewards
        
    
           
def play():
  '''This function plays the complete game and returns the rewards for both the players'''
  
    turn = 1
    board = initial_board()
    p1 = '1'
    p2 = '2'
    while(turn<=9):
        if(turn%2 != 0):
            board = move(board,p1)
        elif(turn%2 == 0):
            board = board = move(board,p2)
        print('Board after move',turn,':',board,'\n')
        turn+=1
    reward1 = reward(board,p1)
    reward2 = reward(board,p2)
    print('The final reward for player 1 is',reward1,'and for player 2 is',reward2)
    return reward1, reward2
                


play()

      

