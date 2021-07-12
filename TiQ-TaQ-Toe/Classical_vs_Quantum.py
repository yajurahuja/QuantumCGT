import numpy as np
import random
from collections import Counter
import functools
import operator
import pickle

from qiskit import QuantumCircuit, QuantumRegister, execute
from qiskit import BasicAer

def initial_board():
    """This is the initial board with amplitude 1 and 0s in all the places"""
    initial_board = [[1,'000000000']]
    return initial_board
    


def action(one_board, player_number):
    """This funnction returns the randomly chosen amplitudes and positions that is to be replaced.
      Eg. amp = [0,1], chosen_zeros = [3,7]
      
      one_board: list (It is a single board from all the possible boards in the list of boards)
                 Eg. [1,'121221112']"""
                 
                 
    zeros = [k for k in range(len(one_board)) if one_board.startswith('0', k)]
    
    possible_boards = []
    for index in zeros:
        possible_boards.append(one_board[:index] + player_number + one_board[index + 1:])
    
    boards_dict = {}
    
    if (len(zeros) == 9):
        for i in possible_boards:
            j = '[' + i.replace('1','1. ').replace('0','0. ').replace('2','-1. ') + ']'
            j = j[:len(j)-2] + j[len(j)-1:]
            boards_dict[i] = j
    else: 
        for i in possible_boards:
            j = '[' + i.replace('1',' 1. ').replace('0',' 0. ').replace('2','-1. ') + ']'
            j = j[:len(j)-2] + j[len(j)-1:]
            boards_dict[i] = j
    
    if (len(zeros) >= 2):
        infile = open("Final_Policy",'rb')
        policy = pickle.load(infile)
  
        mx = 0
        scndmx = 0
        mx_str = ''
        scndmx_str = ''
            
        for i in boards_dict:
            if boards_dict[i] in policy:
                if (policy[boards_dict[i]])>=mx:
                    scndmx = mx
                    scndmx_str = mx_str
                    mx = policy[boards_dict[i]]
                    mx_str = i
                elif policy[boards_dict[i]]>scndmx and mx != policy[boards_dict[i]]:
                    scndmx=policy[boards_dict[i]]
                    scndmx_str = i
        chosen_zeros = []
        pos_1 = [i for i in range(len(mx_str)) if mx_str[i] != one_board[i]]
        chosen_zeros.extend(pos_1)
        pos_2 = [i for i in range(len(scndmx_str)) if scndmx_str[i] != one_board[i]]
        chosen_zeros.extend(pos_2)
        
        if(len(chosen_zeros)==1):
            new_zeros = [x for x in zeros if x not in chosen_zeros]
            a = random.choice(new_zeros)
            chosen_zeros.append(a)
        elif(len(chosen_zeros)==0):
            chosen_zeros = random.sample(set(zeros), 2)
  
        if player_number =='2':
            amp = [1/np.sqrt(2),1/np.sqrt(2)]
            return amp, chosen_zeros
        elif player_number == '1':
            amp = [1,0]
            return amp, chosen_zeros
    elif (len(zeros)==1):
        chosen_zeros = random.sample(set(zeros), 1)
        return chosen_zeros
    else:
        return 'Invalid'
        

def move(board,player_number):
    """"This updates the provided current board to a new board/game position
        board: nested list (current board position)
                Eg. [[1/sqrt(2),'121221112'],[1/sqrt(2),'111221212']]
        player_number: char """
    new_board = []
    
    for i,j in board:
        zeros = [k for k in range(len(j)) if j.startswith('0', k)]
        if (len(zeros)>= 2):
            amp, chosen_zeros = action(j,player_number)
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
            

    #Combining Same Boards
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
    
    #Eliminating boards with no amplitude 
    unwanted = []
    for i in new_board:
        if(i[0]==False):
            unwanted.append(new_board.index(i))
    for ele in sorted(unwanted, reverse = True): 
        del new_board[ele]
        
    #Re-normalizing the board
    a,b = map(list, zip(*new_board))
    a = np.array(a)
    a = list(a/np.linalg.norm(a))

    new_board = [list(i) for i in zip(a,b)]
        
    return new_board


def status(one_board,player_number):
    """This returns 1 if the the player won this board, -1 is opponent won and 0 if it's a draw"""
    
    zeros = [k for k in range(len(one_board)) if one_board.startswith('0', k)]
    opponent_number = '2' if player_number=='1' else '1'
    
    diags = [[one_board[0],one_board[4],one_board[8]],[one_board[2],one_board[4],one_board[6]]]
    rows = [[one_board[0],one_board[1],one_board[2]],[one_board[3],one_board[4],one_board[5]],[one_board[6],one_board[7],one_board[8]]]
    cols =[[one_board[0],one_board[3],one_board[6]],[one_board[1],one_board[4],one_board[7]],[one_board[2],one_board[5],one_board[8]]]
    combined = diags + rows + cols
    
    if(len(zeros)==0):
        if(any(i.count(player_number)==3 for i in combined) and all(i.count(opponent_number)!=3 for i in combined)):
            return 1
        elif (any(i.count(opponent_number)==3 for i in combined) and all(i.count(player_number)!=3 for i in combined)):
            return -1
        else:
            return 0


def reward(board, player_number):
    sum_rewards = 0
    for i,j in board:
        result = status(j,player_number)
        if(result==1):
            sum_rewards += (abs(i**2))*status(j,player_number)*100
    sum_rewards = round(sum_rewards,2)
    return sum_rewards
        
  
           
def play(n):
    
    sum_1 = 0
    for i in range(n):
        turn = 1
        board = initial_board()
        p1 = '1'
        p2 = '2'
        
        while(turn<=9):
            if(turn%2 != 0):
                board = move(board,p1)
            elif(turn%2 == 0):
                board = board = move(board,p2)
            string =''
            for i in board:
                
                if (board.index(i)==(len(board)-1)):           
                    string = string + '('+str(round(i[0].real,2)) + '+' +  str(round(i[0].imag,2)) + 'i'+')' + '|'+ i[1] + '>' 
                else:
                    string = string + '('+str(round(i[0].real,2)) + '+' +  str(round(i[0].imag,2)) + 'i'+')' + '|'+ i[1] + '>'+ ' + '
            #print('Board after move',turn,':\n',string,'\n')
            turn+=1
        reward1 = reward(board,p1)
        reward2 = reward(board,p2)
        print('The final reward for player 1 is',reward1,'and for player 2 is',reward2)
        
        
        if reward1 > reward2:
           sum_1 += 1
    print('Out of all the games, Player 1 has greater probability to win in ',sum_1, 'games and Player 2 in ',n-sum_1,'games.')
        
    #return board
 

play(100)
