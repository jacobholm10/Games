#Jacob Holm
#Sudoku Game


board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]]

def print_board(grid):
    for i in range(len(grid)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - - -")

        for j in range(len(grid[0])):
            if j % 3 == 0:
                print(" | ", end="")
        
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end="")

def find_empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j)




def possible(grid, number, pos):
    #Check rows
    for i in range(len(grid[0])):
        if grid[pos[0]][i] == number and pos[1] != i:
            return False
    
    #Check columns
    for i in range(len(grid)):
        if grid[i][pos[1]] == number and pos[0] != i:
            return False

    #Check squares    
    x = (pos[1] // 3)
    y = (pos[0] // 3)
    for i in range(y*3, y*3 + 3):
        for j in range(x*3, x*3 + 3):
            if grid[i][j] == number and (i, j) != pos:
                return False
    
    return True



def solve(grid):
    found = find_empty(grid)
    if not found:
        return True
    else:
        row, column = found
    
    for i in range(1, 10):
        if possible(grid, i, (row, column)):
            grid[row][column] = i
        
            if solve(grid):
                return True
        
            grid[row][column] = 0


            


print_board(board)
solve(board)
print("_________________________")
print_board(board)


    
