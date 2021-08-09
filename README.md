# How to Play: TiQ-TaQ-Toe

TiQ-TaQ-Toe is a quantum version of the classical Tic Tac Toe game. As in the classical game, this game is played by two players who take turns making their moves, with the "X" player moving first. 

The game starts with a 3x3 grid of empty squares represented as (1 + 0i)|.........> as a quantum state where (1+0i) is the amplitude of the board and the dots represent the empty squares. 

<img src="https://github.com/yajurahuja/QuantumCGT/blob/main/Images/Start.png" alt="alt text" width="500" height="300">

Now, each player can make either a classical move or a quantum move. 

1. **Classical Move:** To make a classical move, the player can simply choose the amplitude 1 from the drop down menu of the square which the player wishes to mark.
 
<img src="https://github.com/yajurahuja/QuantumCGT/blob/main/Images/Classical%20move.png" alt="alt text" width="500" height="300"> 
    
    The new game board after this move would be represented as (1+0i)|X........>. 
    
<img src="https://github.com/yajurahuja/QuantumCGT/blob/main/Images/After%20c-move.png" alt="alt text" width="500" height="300">
    
2. **Quantum Move:** To make a quantum move, the player can select a maximum of two squares to mark by choosing the amplitudes for those squares from the drop down menu. The move should be normalized, i.e. the square of sum of the amplitudes of the squares chosen should be exactly 1. 

  <img src="https://github.com/yajurahuja/QuantumCGT/blob/main/Images/Quantum%20move.png" alt="alt text" width="500" height="300"> 

  This quantum move results in new boards added to the game state. Before this move, our game state was (1+0i)|X........>. The player chose to mark the 5th dot with   amplitude 1/&radic;2 and the 9th dot with amplitude i/&radic;2. Thus, the new game state then becomes (0.71+0i)|X...O....> + (0+0.71i)|X.......O>.

  <img src="https://github.com/yajurahuja/QuantumCGT/blob/main/Images/After%20q-move.png" alt="alt text" width="500" height="300"> 
 

Each player needs to make either a classical or a quantum move for each of the boards that are part of the game state in order to make a legal move. The game ends only after there have been a total of 9 moves played. 

At the end of the game, we will have a game state which consists various game boards with different amplitudes. The end state could look somethinng like (0.0+0.27i)|XXOOOOXXX> + (0.0+0.27i)|XOOXOXXOX> + (0.27+0.0i)|XOXOOXOXX> + (0.0+0.19i)|XOOXXXOXO> + (0.0+0.19i)|XXOXXOOXO> + (0.27+0.0i)|XXOXOXOXO> + (0.0+0.38i)|XOXXOXOXO> + (0.0+0.27i)|XOOOXXXXO> + (-0.27+0.0i)|XXOOXXXOO> + (0.38+0.0i)|XOXXXOOXO> + (-0.27-0.38i)|XOXXOOOXX>. 

Now, this quantum state is measured and a single board, which is the result of the quantum measurement, is chosen at the end. This board determines the outcome of the game. 
If a player succeeds in creating a horizontal, vertical or diagonal line of its marker(X or O) without the opponent creating a line of their own in the same board, the player wins the game. Otherwise, the game ends in a draw. 
<img src="https://github.com/yajurahuja/QuantumCGT/blob/main/Images/result.png" alt="alt text" width="500" height="300">

  





