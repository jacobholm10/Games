import numpy as np

board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]]


def valid(row, column, number):
    global board
    for i in range(0, 9):
        if board[row][i] == number:
            return False
    
    for i in range(0, 9):
        if board[i][column] == number:
            return False
    
    x = (column // 3) * 3
    y = (row // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if board[y + i][x + j] == number:
                return False
    
    return True


def solve_game():
    global board
    for row in range(0, 9):
        for column in range(0, 9):
            if board[row][column] == 0:
                for number in range(1, 10):
                    if valid(row, column, number):
                        board[row][column] = number
                        solve_game()
                        board[row][column] = 0
                
                return
            
    print(np.matrix(board))

solve_game()