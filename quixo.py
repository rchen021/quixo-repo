import random
import math
import time

def check_move(board, turn, index, push_from):
    '''This function checks if a certain move is valid for a certain board.
    It returns True if such a move is valid, False otherwise.'''  
    n = int(math.sqrt(len(board)))
    # if the number on the index is the opponent's number, we return False
    if turn == 2 and board[index] == 1:
        return False
    elif turn == 1 and board[index] == 2:
        return False
    else:
        # if the index is not in the outer ring, we return False
        # check if the index is in the first row
        # check if the index is in the last row
        # check if the index is in the first column, skip the index that has checked
        # check if the index is in the last column, skip the index that has checked
        if index not in list(range(0, n)) and \
            index not in list(range(n ** 2 - n, n ** 2)) and \
            index not in list(range(n, n ** 2 - n, n)) and \
            index not in list(range(2 * n - 1, n ** 2 - n, n)):
            return False
        else:
            # whether the push_from value is valid is checked in the menu
            # if push_from is 'T', index cannot be in the first row
            # if index is not in the first row, we return True, False otherwise
            if push_from == 'T':
                if index not in list(range(0, n)):
                    return True
                else:
                    return False
            # if push_from is 'B', index cannot be in the last row
            # if index is not in the last row, we return True, False otherwise
            elif push_from == 'B':
                if index not in list(range(n ** 2 - n, n ** 2)):
                    return True
                else:
                    return False
            # if push_from is 'L', if index is not in the first column,
            # we return True, False otherwise
            elif push_from == 'L':
                if index not in list(range(0, n ** 2, n)):
                    return True
                else:
                    return False
            # else: push_from is 'R', if index is not in the last column,
            # we return True, False otherwise
            else:
                if index not in list(range(n - 1, n ** 2, n)):
                    return True
                else:
                    return False

def apply_move(board, turn, index, push_from):
    '''This function applies a certain move to the board. It returns
    an updated board according to that move. However, the original 
    board is unchanged.'''    
    # make a copy of the original board
    board_temp = board[:]
    # make board the copy of board_temp, which is the original board,
    # so the change in board_temp will not affect board
    board = board_temp[:]
    # apply move on board_temp, instead of board
    n = int(math.sqrt(len(board)))
    
    if push_from == 'R':
        # pop out the index player wants to move
        board_temp.pop(index)
        # if index is in the first column, index + n - 1 becomes turn
        if index % n == 0:
            board_temp.insert(index + n - 1, turn)
            return board_temp
        # if index is in the first row, last index of the first row becomes turn
        elif index < n:
            board_temp.insert(n - 1, turn)
            return board_temp
        # if index is in the last row, last index of the board becomes turn
        else:
           board_temp.insert(n * n - 1, turn) 
           return board_temp
   
    elif push_from == 'L':
        # if index is in the first row
        if index < n:
            # for all indexes from index to the second index,
            # assign the value on an index to be the value on its left
            for i in range(index, 0, -1):
                board_temp[i] = board_temp[i - 1]
            # assign the value on the first index to be turn
            board_temp[0] = turn
            return board_temp
        # elif index is in the last row
        elif index > n * (n - 1):
            # for all indexes from index to the second index of the last row,
            # assign the value on an index to be the value on its left
            for i in range(index, n ** 2 - n, -1):
                board_temp[i] = board_temp[i - 1]  
            # assign the value on the first index of the last row to be turn
            board_temp[n ** 2 - n] = turn
            return board_temp
        # else: index is in the last column
        else:
            # for all indexes from index to the second index of the index row
            # assign the value on an index to be the value on its left
            for i in range(index, index - n + 1, -1):
                board_temp[i] = board_temp[i - 1]  
            # assign the value on the first index of the index row to be turn
            board_temp[index - n + 1] = turn
            return board_temp
        
    elif push_from == 'T':
        # for all indexes from the index itself to the second top index of the index column, 
        # the value on a index is assigned to be the value on the index above it. 
        for i in range(index, n - 1, -n):
            board_temp[i] = board_temp[i - n]  
        # if index is divisible by n, then index comes from the first column.
        # assign value on the first index to be turn
        if index % n == 0:
            board_temp[0] = turn
        # elif index has remainder n - 1 when divides by n, 
        # then index comes from the last column of the board.
        # assign value on the first index of the last column, which is index n - 1, to be turn
        elif index % n == n - 1:
            board_temp[n - 1] = turn   
        # else: the index comes from the last row
        # assign value on the first index of the index column to be turn
        else:
            board_temp[index - n * (n - 1)] = turn
        return board_temp
    
    else:
        # for all indexes from the index itself to the second last index of the index column, 
        # the value on a index is assigned to be the value on the index below it. 
        for i in range(index, n * (n - 1) , n):
            board_temp[i] = board_temp[i + n] 
        # if index is divisible by n, then index comes from the first column.
        # assign value on the last index of the first column to be turn            
        if index % n == 0:
            board_temp[n * (n - 1)] = turn
        # elif index has remainder n - 1 when divides by n, 
        # then index comes from the last column of the board.
        # assign value on the last index of the last column to be turn
        elif index % n == n - 1:
            board_temp[n * n - 1] = turn
        # else: the index comes from the first row
        # assign value on the last index of the index column to be turn
        else:
            board_temp[index + n * (n - 1)] = turn
        return board_temp

def check_victory(board, who_played):
    '''This function checks if a victory situation has been reached.
    It will return 0 if no winning situation is present for this game;
    1 if player 1 wins; and 2 if player 2 wins.'''
    
    n = int(math.sqrt(len(board)))
    # initiate player value and index values
    # player_1 turns to 1 when there is a line of 1
    # player_2 turns to 2 when there is a line of 2
    player_1 = 0
    player_2 = 0
    a = 0
    b = n
    # while loop checks if any horizontal line has a row of 1 or 2 
    # loop ends when b is greater than n * n
    while b <= n * n:
        # initiate total value
        # reset total value for each loop
        total = 0
        # for all indexes in a certain row, except the last index
        for i in range(a, b - 1):
            # if the value on an index is the same as the value on its right and
            # the value is not zero, total = total + value
            if board[i] == board[i + 1] and board[i] != 0:
                total += board[i]
                # if index reaches the second last index of a row,
                # total = total + value on the last index
                if i == b - 2:
                    total += board[i + 1]
            # else: the row is not a row of 1 nor 2
            # set total to zero
            else:
                total == 0
                break
        # both a and b increase by n, 
        # so we can move to the next row in the next loop
        a += n
        b += n
        # check if there is a row of 1 or 2
        # if total = n, the row has a line of 1
        if total == n:
            player_1 = 1   
        # if total = 2n, the row has a line of 2
        if total == 2 * n:
            player_2 = 2
    
    # reset index values        
    a = 0
    b = n * (n - 1)
    # while loop checks if any vertical line has a column of 1 or 2 
    # loop ends when a = n
    while a <= n - 1:
        # reset total value
        total = 0
        # for all indexes in a certain column, except the last index
        for i in range(a, b, n):
            # if the value on an index is the same as the value below it and
            # the value is not zero, then total = total + value
            if board[i] == board[i + n] and board[i] != 0:
                total += board[i]
                # if index reaches the second last index of a column,
                # total = total + value on the last index
                if i == b - n:
                    total += board[i + n]
            else:
                total == 0
                break
        # both a and b increase by 1, 
        # so we can move to the next column in the next loop
        a += 1
        b += 1
        if total == n:
            player_1 = 1         
        if total == 2 * n:
            player_2 = 2
    
    # reset total value
    total = 0
    # for loop checks if the downward diagonal line has a line of 1 or 2
    # for all indexes on the downward diagonal line, except the last index
    for i in range(0, n * n - n, n + 1):
        # if the value on an index is the same as the value on the next index and
        # the value is not zero, then total = total + value
        if board[i] == board[i + n + 1] and board[i] != 0:
            total += board[i]
            # if index reaches the second last index of the diagonal line,
            # total = total + value on the last index
            if i == (n + 1) * (n - 2):
                total += board[n * n - 1]           
        else:
            total == 0
            break
    if total == n:
        player_1 = 1
    if total == 2 * n:
        player_2 = 2
        
    total = 0
    # for loop checks if the upward diagonal line has a line of 1 or 2
    # for all indexes on the upward diagonal line, except the last index
    for i in range(n - 1, n * n - n, n - 1):
        # if the value on an index is the same as the value on the next index and
        # the value is not zero, then total = total + value
        if board[i] == board[i + n - 1] and board[i] != 0:
            total += board[i]
            # if index reaches the second last index of the diagonal line,
            # total = total + value on the last index
            if i == (n - 1) ** 2:
                total += board[n * n - n]
        else:
            total == 0    
            break
    if total == n:
        player_1 = 1
    if total == 2 * n:
        player_2 = 2
    
    # check who wins
    # if both players form a line at the very same time,
    # then the player who played that move loses the game.
    if player_1 == 1 and player_2 == 2:
        if who_played == 1:
            return 2
        else:
            return 1
    # else: 3 cases: if player_1 = 1, player_1 wins, return 1.
    # if player_2 = 2, player_2 wins, return 2.
    # Otherwise, no one wins, return 0
    else:
        if player_1 == 1:
            return 1
        elif player_2 == 2:
            return 2
        else:
            return 0

def computer_move(board, turn, level):   
    n = int(math.sqrt(len(board)))
    def check_opp_win(board, turn):
        '''This function checks if player can win with certain moves. 
        It returns True if one can win, False otherwise.'''
        
        for i in range(0, n * n):
            if board[i] == 3 - turn:
                continue
            else:
                if check_move(board, turn, i, 'T'):
                    board_update = apply_move(board, turn, i, 'T')  
                    if check_victory(board_update, turn) == turn:
                        return True
                        
                if check_move(board, turn, i, 'B'):
                    board_update = apply_move(board, turn, i, 'B')                    
                    if check_victory(board_update, turn) == turn:
                        return True
                        
                if check_move(board, turn, i, 'L'):
                    board_update = apply_move(board, turn, i, 'L')
                    if check_victory(board_update, turn) == turn:
                        return True
                        
                if check_move(board, turn, i, 'R'):
                    board_update = apply_move(board, turn, i, 'R')
                    if check_victory(board_update, turn) == turn:
                        return True
        return False   
    
    if level == 1:      # computer level 1  
        while True:
            x = random.randint(1, 4) # generate a random integer between 1 and 4
            if x == 1:
                push_from = 'T' # 1 represents push_from 'T'
            elif x == 2:
                push_from = 'B'
            elif x == 3:
                push_from = 'L'
            else:
                push_from = 'R'
            # generate a random index between 0 and n * n - 1
            index = random.randint(0, n * n - 1)
            # if the move is valid, return index and push_from
            if check_move(board, turn, index, push_from):
                return (index, push_from)
            
    # initiate a list of index needs to be avoided and a list can play
    list_avoid = []
    list_can_play = []
    list_avoid_direct_win = []
    
    if level == 2:
        # for all indexes on the board, starting from 0
        for i in range(0, n * n):
            # if the value on the index is opponent's number, skip that index
            if board[i] == 3 - turn:
                continue
            else: # check if push_from is valid
                # if the move is valid, append (i, 'T') to list_can_play
                if check_move(board, turn, i, 'T'):
                    list_can_play.append((i, 'T'))
                    # assign board_update to the updated board according to that move
                    board_update = apply_move(board, turn, i, 'T')
                    # if computer wins, we return the index and push_from
                    if check_victory(board_update, turn) == turn:
                        return (i, 'T')
                    # if the move leads to opponent's win or opponent will be 
                    # able to win in his next move, we append index and 
                    # push_from to list_avoid
                    if check_victory(board_update, turn) == 3 - turn or \
                        check_opp_win(board_update, 3 - turn) == True:
                        list_avoid.append((i, 'T'))
                    if check_victory(board_update, turn) == 3 - turn:
                        list_avoid_direct_win.append((i, 'T'))
                    
                if check_move(board, turn, i, 'B'):
                    list_can_play.append((i, 'B'))
                    board_update = apply_move(board, turn, i, 'B')                    
                    if check_victory(board_update, turn) == turn:
                        return (i, 'B')
                    if check_victory(board_update, turn) == 3 - turn or \
                        check_opp_win(board_update, 3 - turn) == True:
                        list_avoid.append((i, 'B'))
                    if check_victory(board_update, turn) == 3 - turn:
                        list_avoid_direct_win.append((i, 'B'))
                                         
                if check_move(board, turn, i, 'L'):
                    list_can_play.append((i, 'L'))
                    board_update = apply_move(board, turn, i, 'L')
                    if check_victory(board_update, turn) == turn:
                        return (i, 'L')
                    if check_victory(board_update, turn) == 3 - turn or \
                        check_opp_win(board_update, 3 - turn) == True:
                        list_avoid.append((i, 'L'))
                    if check_victory(board_update, turn) == 3 - turn:
                        list_avoid_direct_win.append((i, 'L'))
                                       
                if check_move(board, turn, i, 'R'):
                    list_can_play.append((i, 'R'))
                    board_update = apply_move(board, turn, i, 'R')
                    if check_victory(board_update, turn) == turn:
                        return (i, 'R')
                    if check_victory(board_update, turn) == 3 - turn or \
                        check_opp_win(board_update, 3 - turn) == True:
                        list_avoid.append((i, 'R'))
                    if check_victory(board_update, turn) == 3 - turn:
                        list_avoid_direct_win.append((i, 'R'))
    
    # if whatever moves computer make will lead to opponent's win in this or next round
    if len(list_avoid) == len(list_can_play):
        # if whatever moves computer make will lead opponent to win directly,
        # return a random move
        if len(list_avoid_direct_win) == len(list_can_play):
            return computer_move(board, turn, 1)
        else: # apply moves that do not lead to a direct win of the opponent 
            # remove all (index, push_from) in list_can_play which are also
            # in list_avoid_direct_win    
            for i in list_avoid_direct_win:
                list_can_play.remove(i)
            # generate a random integer with the range of all index numbers in list
            choose_one = random.randint(0, len(list_can_play) - 1)
            # return the move according to that index
            return list_can_play[choose_one]
    else: # there are(is) moves that do not lead opponent to win in this or next round
        # remove all combinations of index and push_from that need to be avoided
        # in list_can_play
        for i in list_avoid:
            list_can_play.remove(i)
        choose_one = random.randint(0, len(list_can_play) - 1)
        return list_can_play[choose_one]
    
def display_board(board):
    '''This function displays the board. It returns nothing.'''
    
    n = int(math.sqrt(len(board)))
    # for integers from 0 to n - 1
    for i in range(0, n):
        # for indexes from the first column to the last column
        for a in range(i * n, i * n + n):
            print(board[a], end = ' ')
        print() # change to a new line
        
def menu():  
    board = [0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0]
    n = int(math.sqrt(len(board)))
    print('Welcome to Quixo!!')  
    print('\nNote: If you want to end the game, press "E" to exit.')
    
    while True: # if the input is not '1' or '2', continue the loop
        # opptype represents the type of opponent player wants to choose
        opptype = input('\nDo you want to play with the computer or another human?\n1: computer\n2: human\nEnter 1 or 2: ')
        if opptype == '1' or opptype == '2':
            break
        elif opptype.capitalize() == 'E':
            print('\nThe Game will end in 3 seconds!')
            time.sleep(3)
            return 
        else:
            print('\nEnter correct value!')        
    # player 1 will always play first      
    turn = 1 # initiate the value of turn to 1     
          
    if opptype == '1': # if player choose to play with computer  
        # ask what level player wants to play
        # if the input is not '1' or '2', continue the loop.
        while True:
            level = input('\nWhat level of computer player do you want to challenge?\nEnter 1 or 2: ')
            if level == '1' or level == '2':
                break
            elif level.capitalize() == 'E':
                print('\nThe Game will end in 3 seconds!')
                time.sleep(3)
                return
            else:
                print('\nEnter correct value!')
        level = int(level) # change input string to integer 
    print()   
    display_board(board) # show the original board first to begin the game  
                 
    while True: 
        if opptype == '2':
            print('\nPlayer', turn, "'s turn")
        if opptype == '1':
            print('\nMy turn')       
        # this while loop continues until the combination of index and push_from is valid
        while True: 
            while True:
                # if all the characters in the input are digits, break the loop
                # otherwise, continue the loop
                while True:
                    index = input('Enter index: ')
                    if index.isdigit():
                        break
                    elif index.capitalize() == 'E':
                        print('\nThe Game will end in 3 seconds!')
                        time.sleep(3)
                        return
                    else:
                        print('\nEnter valid value!')
                index = int(index)  # turn input string into integer
                # if the index is in the outer ring, break the loop                          
                if index in list(range(0, n)) or \
                    index in list(range(n ** 2 - n, n ** 2)) or \
                    index in list(range(n, n ** 2, n)) or \
                    index in list(range(n - 1, n ** 2, n)):
                    break
                else:
                    print('\nEnter correct value!')
            
            # if push_from is "T", "B", "L", or "R", break the loop
            # otherwise, continue the loop    
            while True:
                push_from = (input('Enter "T", "B", "L", or "R": ')).capitalize()
                if push_from == 'B' or push_from == 'L' or \
                    push_from == 'T' or push_from == 'R':
                        break
                elif push_from == 'E':
                    print('\nThe Game will end in 3 seconds!')
                    time.sleep(3)
                    return
                else:
                    print('\nPlease enter correct letter!')           
            if check_move(board, turn, index, push_from) == True:
                break
            else:
                print('\nPlease enter valid value!')  
                
        # update the board with the valid move applied in place                
        board = apply_move(board, turn, index, push_from)
        print()
        display_board(board)
            
        if check_victory(board, turn) == 0:
            # for human vs. human, change the value of turn, so the next player can play
            if opptype == '2':
                turn = 3 - turn
                continue 
        else:
            # if human vs. computer
            if opptype == '1':
                # check who wins
                if check_victory(board, turn) == 1:
                    print("\nYou are the winner!")
                    print('\nThe Game will end in 5 seconds!')
                    time.sleep(5)
                    break
                else:
                    print('\nComputer is the winner!')
                    print('\nThe Game will end in 5 seconds!')
                    time.sleep(5)
                    break
            # else: for human vs. human, the winner is the output of check_victory
            else:
                print('\nThe winner is Player', check_victory(board, turn), '!')
                print('\nThe Game will end in 5 seconds!')
                time.sleep(5)
                break
        # if human vs. computer, apply computer move                 
        if opptype == '1':
            print("\nComputer's turn")
            a = computer_move(board, 3 - turn, level)
            # print the move computer is going to play
            print(a)
            index = a[0]
            push_from = a[1]
            # apply the move on the board
            board = apply_move(board, 3 - turn, index, push_from)
            print()
            display_board(board)
            # check winning situation
            # if no one wins, continue
            if check_victory(board, turn) == 0:
                continue          
            else: # print who wins
                if check_victory(board, turn) == 1:
                    print("\nYou are the winner!")
                    print('\nThe Game will end in 5 seconds!')
                    time.sleep(5)
                    break
                else:
                    print('\nComputer is the winner!')
                    print('\nThe Game will end in 5 seconds!')
                    time.sleep(5)
                    break                        
        
if __name__ == "__main__":
    menu()


    
