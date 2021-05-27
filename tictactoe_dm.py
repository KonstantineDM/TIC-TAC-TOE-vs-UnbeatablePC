# Programmer: Konstantin Davydov
# Date of creation: 2021.05.03

import sys
import time

"""
Unbeatable TIC-TAC-TOE game vs Computer
"""

# global variables
def global_vars():
    global empty_cell, hum_token, comp_token, turn, total_cells, legal_moves, turn_value
    empty_cell = ' '
    hum_token = 'X'
    comp_token = 'O'
    total_cells = 9
    legal_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    turn_value = (5, 1, 3, 7, 9, 2, 4, 6, 8)

def rules():
    print('''
Welcome to the game TIC-TAC-TOE where you play against the computer.
***WARNING! THE COMPUTER IS IMPOSSIBLE TO BEAT!***


This is the game board with numerated cells:

  1  |  2  |  3
-----------------
  4  |  5  |  6
-----------------
  7  |  8  |  9

You play by placing your token ('X' or 'O')  in board's cells.
The first player, picks 'X' as theirs token.
The game continues until one of the players fills the whole row
(horizontal, vertical or diagonal) with tokens of chosen type.
    ''')

def ask_yes_no():
    """
    gives the user a simple question with a yes/no answer, returns user's input
    """
    answer = input().lower()
    return answer

def board_empty():
    """
    creates a clear board with 9 empty cells
    """
    board = [empty_cell for i in range(total_cells)]
    return board

def game_board(board):
    """
    shows a game board with all turns made so far
    """
    print('  ' + board[0] + '  |  ' + board[1] + '  |  ' + board[2] + '  ')
    print('-----------------')
    print('  ' + board[3] + '  |  ' + board[4] + '  |  ' + board[5] + '  ')
    print('-----------------')
    print('  ' + board[6] + '  |  ' + board[7] + '  |  ' + board[8] + '  ' + '\n')
    
def turn_order():
    print('\nDo you want to take the first turn?')
    print('Enter \'yes\', \'no\' or enter \'quit\' to exit game.')
    answer = ask_yes_no()
    while answer not in ['yes', 'no', 'quit']:
        print('\nPlease make your choice: ', end='')
        answer = ask_yes_no()
    if answer == 'yes':
        hum_token = 'X'
        comp_token = 'O'
    elif answer == 'no':
        comp_token = 'X'
        hum_token = 'O'
    elif answer == 'quit':
        print('Goodbye!')
        input('Press Enter to exit.')
        sys.exit()
    turn = 'X'
    return turn, hum_token, comp_token

def human_turn(board, hum_token):
    """
    makes a human player's turn, changes the board accordingly
    """
    while True:
        try:
            human_turn = input('\nEnter the number of the gameboard cell you want to \n'
                               'place your token in (or enter "quit" to exit):\n')
            if human_turn == 'quit':
                print('\nGoodbye!')
                sys.exit()
            human_turn = int(human_turn)
            if human_turn in legal_moves:
                board[human_turn - 1] = hum_token
                legal_moves.remove(human_turn)
                break
            elif human_turn not in list(range(total_cells)) and human_turn not in legal_moves:    
                print('\nThere is no such cell.', end='')
                continue
            elif human_turn == 'quit':
                print('\nGoodbye!')
                input('Press Enter to exit.')
                sys.exit()
            elif board[human_turn - 1] in ('X', 'O'):
                print('\nCell already occupied.', end='')
                continue
        except ValueError:
            print('\nImpossible choice value!', end='')
            continue

def comp_turn(board, turn, hum_token, comp_token, turn_value, legal_moves):
    # computer's turn with simulating thinking process (time.sleep)
    print('My turn now! Hmm, let me think', end='', flush=True)
    for i in range(3):
        time.sleep(0.7)
        print('.', end='', flush=True)
    time.sleep(0.5)
    print(' Here is my turn:', flush=True); time.sleep(0.7)
    for token in (comp_token, hum_token):
        for value in turn_value:
            if value in legal_moves:
                board_check = board[:]
                board_check[value - 1] = token
                if iswinner(board_check, token):
                    board[value - 1] = comp_token
                    legal_moves.remove(value)
                    return
    if not iswinner(board, turn):
        for value in turn_value:
            if value in legal_moves:
                board[value - 1] = comp_token
                legal_moves.remove(value)
                return

def pass_turn(turn):
    if turn == 'X':
        turn = 'O'
    elif turn == 'O':
        turn = 'X'
    return turn

def iswinner(board, turn):
    # check if a winner is defined
    wins = ((1, 2, 3),      # all possible win combinations
            (4, 5, 6),
            (7, 8, 9),
            (1, 4, 7),
            (2, 5, 8),
            (3, 6, 9),
            (1, 5, 9),
            (3, 5, 7))
    winner = ''
    for row in wins:
        if board[row[0] - 1] == board[row[1] - 1] == board[row[2] - 1] == turn:
            winner = turn
    return winner or False

def congrat(winner):
    # congratulate the winner
    if winner == comp_token:
        print('\n' + '-' * 60)
        print('I won, human! Expectedly.')
        print('-' * 60)
    if winner == hum_token:
        print('\n' + '-' * 60)
        print('You won the game against the computer! Congratulations!')
        print('-' * 60)

def start_again():
    # start the game again
    print('Do you want to start a new game? Enter \'yes\' or \'no\': ', end='')
    return ask_yes_no()

def main():
    global_vars()
    rules()
    board = board_empty()
    turn, hum_token, comp_token = turn_order()
    while not iswinner(board, turn) and empty_cell in board:
        if turn == hum_token:
            human_turn(board, hum_token)
            game_board(board)
            if iswinner(board, turn) == hum_token:
                congrat(hum_token)
                break
            turn = pass_turn(turn)
            continue
        if turn == comp_token:
            comp_turn(board, turn, hum_token, comp_token, turn_value, legal_moves)
            game_board(board)
            if iswinner(board, turn):
                congrat(comp_token)
                break
            turn = pass_turn(turn)
            continue
    if empty_cell not in board:
        print('-' * 60)
        print('The game is a DRAW!')
        print('-' * 60)
    again = start_again()
    while again.lower() not in ('yes', 'no'):
        again = start_again()
    if again.lower() == 'yes':
        main()
    else:
        print('\nGoodbye!')
        input('Press Enter to exit.')
        sys.exit()


if __name__ == '__main__':
    main()
