
# coding: utf-8

# In[28]:

from __future__ import print_function 
from IPython.display import clear_output
def display_board(board):
    clear_output()
    
    print(' '+board[7]+' '+'|'+' '+board[8]+' '+'|'+' '+board[9])
    print('-----------')
    
    print(' '+board[4]+' '+'|'+' '+board[5]+' '+'|'+' '+board[6])
    print('-----------')  
    
    print(' '+board[1]+' '+'|'+' '+board[2]+' '+'|'+' '+board[3])


# In[29]:

def player_input():
    marker = ''
    while not (marker=='X' or marker == 'O'):
        marker = raw_input('choose your marker x or o:').upper()
    if marker == 'x':
        return ('X','O')
    else:
        return ('O','X')
            
        


# In[30]:

def place_marker(board,marker,position):
    board[position] = marker


# In[42]:

def win_check(board,marker):
    return ((board[7] == marker and board[8] == marker and board[9] == marker) or # across the top
    (board[4] == marker and board[5] == marker and board[6] == marker) or # across the middle
    (board[1] == marker and board[2] == marker and board[3] == marker) or # across the bottom
    (board[7] == marker and board[4] == marker and board[1] == marker) or # down themarkft side
    (board[8] == marker and board[5] == marker and board[2] == marker) or # down the middle
    (board[9] == marker and board[6] == marker and board[3] == marker) or # down the right side
    (board[7] == marker and board[5] == marker and board[3] == marker) or # diagonal
    (board[9] == marker and board[5] == marker and board[1] == marker)) # diagonal
    


# In[32]:

import random
def choose_first():
    if random.randint(0,1) == 1:
        return 'Player 1'
    else:
        return 'Player 2'


# In[38]:

def space_check(board,position):
    return board[position] == ' '


# In[44]:

def full_board_check(board):
    for i in range(1,10):
        if space_check(board,i):
            return False
        
    return True


# In[35]:

def player_choice(board):
    position = ''
    while position not in '1 2 3 4 5 6 7 8 9'.split() or not space_check(board,int(position)):
        
        position = raw_input('choose your next position(1-9) ')
    return int(position)


# In[36]:

def replay():
    
    return raw_input('Do you want to play again? Enter Yes or No: ').lower().startswith('y')


# In[ ]:

print('Welcome to Tic Tac Toe!')

while True:
    # Reset the board
    theBoard = [' '] * 10
    player1_marker, player2_marker = player_input()
    turn = choose_first()
    print(turn + ' will go first.')
    game_on = True

    while game_on:
        if turn == 'Player 1':
            # Player1's turn.
            
            display_board(theBoard)
            position = player_choice(theBoard)
            place_marker(theBoard, player1_marker, position)

            if win_check(theBoard, player1_marker):
                display_board(theBoard)
                print('Congratualtions! You have won the game!')
                game_on = False
            else:
                if full_board_check(theBoard):
                    display_board(theBoard)
                    print('The game is a draw!')
                    break
                else:
                    turn = 'Player 2'

        else:
            # Player2's turn.
            
            display_board(theBoard)
            position = player_choice(theBoard)
            place_marker(theBoard, player2_marker, position)

            if win_check(theBoard, player2_marker):
                display_board(theBoard)
                print('Player 2 has won!')
                game_on = False
            else:
                if full_board_check(theBoard):
                    display_board(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'Player 1'

    if not replay():
        break


# In[ ]:



