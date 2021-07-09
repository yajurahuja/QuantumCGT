
import numpy as np
import random
from collections import Counter
import functools
import operator
import gui

from PyQt5.QtWidgets import *
from qiskit import QuantumCircuit, QuantumRegister, execute
from qiskit import BasicAer


amplitudes = {'0': 0, '1': 1, '-1': -1, 'i': 1j , '-i': -1j , '1/\u221A2': 1/np.sqrt(2), '-1/\u221A2': -1/np.sqrt(2), 'i/\u221A2': 1j/np.sqrt(2), '-i/\u221A2':  -1j/np.sqrt(2)}

def current_statestring(board):
    string =''
    for i in board:
        if (board.index(i)==(len(board)-1)):           
            string = string + '('+str(round(i[0].real,2)) + '+' +  str(round(i[0].imag,2)) + 'i'+')' + '|'+ i[1] + '>' 
        else:
            string = string + '('+str(round(i[0].real,2)) + '+' +  str(round(i[0].imag,2)) + 'i'+')' + '|'+ i[1] + '>'+ ' + '
    return string

def initial_board():
    """This is the initial board with amplitude 1 and 0s in all the places"""
    initial_board = [[1,'000000000']]
    return initial_board   
    

def action(one_board):
    """This funnction returns the randomly chosen amplitudes and positions that is to be replaced.
      Eg. amp = [0,1], chosen_zeros = [3,7]
      
      one_board: list (It is a single board from all the possible boards in the list of boards)
                 Eg. [1,'121221112']"""
                
    print("\nThe current board you are working with is ",one_board,'\n')
    #amplitudes = [0, 1, -1 , 1j, -1j, 1/np.sqrt(2), -1/np.sqrt(2), 1j/np.sqrt(2), -1j/np.sqrt(2)]
    
    print(amplitudes)
    zeros = [k for k in range(len(one_board)) if one_board.startswith('0', k)]
    if (len(zeros)>= 2):
        a1 = int(input("Choose the first index (1-9) of amplitude you want for this board: "))
        c1 = int(input("Choose the first index (1-9) of the position you want to fill in this board: "))
        while (c1-1 not in zeros):
            print('Invalid move. Try again.')
            c1 = int(input("Choose the first index (1-9) of the position you want to fill in this board: "))
        a2 = int(input("Choose the second index (1-9) of amplitude you want for this board: "))
        c2 = int(input("Choose the second index (1-9) of the position you want to fill in this board: "))
        
        zeros.remove(c1-1)

        while (c2-1 not in zeros):
            print('Invalid move. Try again.')
            c2 = int(input("Choose the second index (1-9) of the position you want to fill in this board: "))
        
        i = amplitudes[a1-1]
        j = amplitudes[a2-1]
        while not(round((abs(i)**2 + abs(j**2)),1)==1 or (abs(i)**2 + abs(j**2))==1):
            print("Invalid choice of amplitudes. The total probability of the boards is not 1. Fill in new amplitudes")
            a1 = int(input("Choose the first index (1-9) of amplitude you want for this board: "))
            a2 = int(input("Choose the second index (1-9) of amplitude you want for this board: "))
            i = amplitudes[a1-1]
            j = amplitudes[a2-1]
        
        amp = [amplitudes[a1-1],amplitudes[a2-1]]
        chosen_zeros = [c1-1,c2-1]
        return amp, chosen_zeros
    elif (len(zeros)==1):
        chosen_zeros = random.sample(set(zeros), 1)
        return chosen_zeros
    else:
        return 'Invalid'
    

def action_Gui(board, boards, boxes, amps):
    amp = []
    chosen_zeros = []
    for i in range(len(boards)):
        if boards[i] == board:
            chosen_zeros.append(boxes[i])
            amp.append(amplitudes[amps[i]])
    return amp, chosen_zeros


def move_Gui(board, player_number, player_name, turn, current_board, widget, app):

    """"This updates the provided current board to a new board/game position
        board: nested list (current board position)
                Eg. [[1/sqrt(2),'121221112'],[1/sqrt(2),'111221212']]
        player_number: char """
    amplist = [str(i) for i,j in board]
    boardlist = [j for i,j in board]
    widget.addWidget(gui.TicTacToeWindow(widget, player_number, player_name, turn, boardlist, current_board, amplist))
    widget.setCurrentIndex(widget.currentIndex() + 1)
    widget.show()
    app.exec()
    boards, boxes, amps = widget.currentWidget().return_data()
    new_board = []
    for i,j in board:
        zeros = [k for k in range(len(j)) if j.startswith('0', k)]
        if (len(zeros)>= 2):
            amp, chosen_zeros = action_Gui(j, boards, boxes, amps)
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


       

# def move(board,player_number):
#     """"This updates the provided current board to a new board/game position
#         board: nested list (current board position)
#                 Eg. [[1/sqrt(2),'121221112'],[1/sqrt(2),'111221212']]
#         player_number: char """
#     new_board = []
#     for i,j in board:
#         zeros = [k for k in range(len(j)) if j.startswith('0', k)]
#         if (len(zeros)>= 2):
#             amp, chosen_zeros = action(j)
#             new_amplitudes = [round((element*i).real,2)+round((element*i).imag,2)*1j for element in amp]
#             new_positions = []
#             for index in chosen_zeros:
#                 new_positions.append(j[:index] + player_number + j[index + 1:])
#             current_board = [list(a) for a in zip(new_amplitudes, new_positions)]
#             new_board.extend(current_board)
#             #print('Initital:',i,j,'\nRandom Apms: ', amp, '\nRandom Positions: ',chosen_zeros,'\nNew Apms: ',new_amplitudes, '\nNew Positions: ',new_positions, '\nCurrent Board: ',current_board,'\n\n\n')
#         elif (len(zeros)==1):
#             for index in zeros:
#                 new_positions = j[:index] + player_number + j[index + 1:]
#             current_board = [[i, new_positions]]
#             new_board.extend(current_board)
#         else:
#             new_board = board 

#     #Combining Same Boards
#     flat = functools.reduce(operator.iconcat, new_board, [])
#     duplicate_items = ([item for item, count in Counter(flat).items() if (count > 1 and type(item)==str)])
    
#     concatenated_list = []
#     all_indexes = []
#     for i in duplicate_items:
#         indexes = []
#         for j in new_board:
#             if (i==j[1]):
#                 indexes.append(new_board.index(j))
#                 all_indexes.append(new_board.index(j))
#         total_amp = 0
#         for k in indexes:
#             total_amp += new_board[k][0]
#         combined_ele = [total_amp,i]
#         concatenated_list.append(combined_ele)

#     for ele in sorted(all_indexes, reverse = True): 
#             del new_board[ele]   
#     new_board.extend(concatenated_list)
    
#     #Eliminating boards with no amplitude 
#     unwanted = []
#     for i in new_board:
#         if(i[0]==False):
#             unwanted.append(new_board.index(i))
#     for ele in sorted(unwanted, reverse = True): 
#         del new_board[ele]
    
#     #Re-normalizing the board
#     a,b = map(list, zip(*new_board))
#     a = np.array(a)
#     a = list(a/np.linalg.norm(a))

#     new_board = [list(i) for i in zip(a,b)]
        
#     return new_board


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
        
    
           
def play(player_names, widget, app):
    turn = 1
    board = initial_board()
    p1 = '1'
    p2 = '2'
    while(turn<=9):
        if(turn%2 != 0):
            board = move_Gui(board,p1, player_names[0], turn, current_statestring(board), widget, app)
        elif(turn%2 == 0):
            board = move_Gui(board,p2, player_names[1], turn, current_statestring(board), widget, app)
        string =''
        for i in board:
            
            if (board.index(i)==(len(board)-1)):           
                string = string + '('+str(round(i[0].real,2)) + '+' +  str(round(i[0].imag,2)) + 'i'+')' + '|'+ i[1] + '>' 
            else:
                string = string + '('+str(round(i[0].real,2)) + '+' +  str(round(i[0].imag,2)) + 'i'+')' + '|'+ i[1] + '>'+ ' + '
        print('Board after move',turn,':\n',string,'\n\n')
        turn+=1
    reward1 = reward(board,p1)
    reward2 = reward(board,p2)
    print('The final reward for player 1 is',reward1,'and for player 2 is',reward2)
    return board
                

def measure(player_names, widget, app):
    board = play(player_names, widget, app)
    q1 = np.array([1,0])
    q2 = np.array([0,1])
    l = []
    for i in board:
        tensor_product = np.array([1])
        for j in i[1]:
            if(j=='1'):
                tensor_product = np.kron(tensor_product,q1)
            elif(j=='2'):
                tensor_product = np.kron(tensor_product,q2)
        i1 = list(tensor_product).index(1)
        i2 = i[0]
        l.append([i2,i1])
    statevector = [0]*(2**9)
    for i,j in l:
        #print(i,j)
        statevector[j] = i
    normalised = statevector/np.linalg.norm(statevector)
    
    q = QuantumRegister(9)
    qc = QuantumCircuit(q)
    qc.initialize(normalised, [q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8]])
    qc.measure_all()
    
    #a = execute(qc, backend=BasicAer.get_backend('qasm_simulator')).result().get_counts()
    measurement = execute(qc, backend=BasicAer.get_backend('qasm_simulator'),shots=1).result().get_counts()
    for i in measurement:
        j = i.replace('1','2')
        result = j.replace('0','1')
    player_number = '1'
    state = status(result,player_number)
    
    if state == 1:
        print('The final board is ',result,'\nPlayer 1 wins!!!')
    elif state == -1:
        print('The final board is ',result,'\nPlayer 2 wins!!!')
    elif state == 0:
        print('The final board is',result,'\nIt\'s a draw.')

def setup_GUI():
    widget = QStackedWidget()
    widget.setWindowTitle("Quantum TicTacToe")
    window = gui.MainWindow(widget)
    widget.addWidget(window)
    widget.show()

    return widget

#measure()

 







    
