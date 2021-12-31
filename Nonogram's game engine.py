"""Nonogram's workings"""
import numpy as np

cross = {0: 5, 1: 1, 5:5}
grid = np.zeros((10,10), dtype=int)
# grid_check = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], '1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], '10': []}

'''Stage 56: Medium Difficulty for test'''
grid_check = {'a': [[[2], False]], 'b': [[[1, 3, 1], False]], 'c': [[[7], False]], 'd': [[[1, 7], False]], 'e': [[[9], False]], 'f': [[[8], False]], 'g': [[[9], False]], 'h': [[[1, 7], False]], 'i': [[[1, 3, 1], False]], 'j': [[[1, 1], False]], '1': [[[3], False]], '2': [[[5], False]], '3': [[[3], False]], '4': [[[8], False]], '5': [[[6], False]], '6': [[[10], False]], '7': [[[9], False]], '8': [[[9], False]], '9': [[[3, 2], False]], '10': [[[3, 2], False]]}
tiles = 63
conditions_pos = {0: [False,1], 1: [False,1], 2: [False,1] , 3: [False,1] , 4: [False,1] , 5: [False,1], 6: [False,1], 7: [False,1], 8: [False,1] , 9: [True,0]}
conditions_neg = {0: [True,0], 1: [False,-1], 2: [False,-1] , 3: [False,-1] , 4: [False,-1] , 5: [False,-1], 6: [False,-1], 7: [False,-1], 8: [False,-1] , 9: [False,-1]}

def solution(): # Solution to Stage 56: Medium Difficulty for test
    '''compare game grid to solution grid'''    
    return [[0,0,0,0,1,1,1,0,0,0],
        [5,5,0,1,1,1,1,1,5,5],
        [0,5,0,5,1,1,1,0,5,0],
        [0,1,1,1,1,1,1,1,1,0],
        [0,5,1,1,1,1,1,1,0,5],
        [1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,0],
        [5,1,1,1,1,1,1,1,1,1],
        [5,5,1,1,1,0,1,1,0,5],
        [0,1,1,1,5,5,5,1,1,0]]

def gameover(grid_check):
    '''If all values return True it quits'''
    for value in grid_check.values():
        if value[0][1] == False:
            return False
    print("Game Quit Successfully")
    return True

def finish(grid, r_index, c_index, neg, pos, cross):
    '''When a cell completes a row and column, this piece runs'''
    i,j = r_index, c_index
    up, down, left, right = i,i,j,j
    up_d, down_d, left_d, right_d = False, False, False, False
    while (up_d & down_d & left_d & right_d) == False:
        grid[up][j],grid[down][j] = cross[grid[up][j]], cross[grid[down][j]]
        grid[i][left],grid[i][right] = cross[grid[i][left]],cross[grid[i][right]]
        up_d, down_d = neg[up][0], pos[down][0]
        up, down = up + neg[up][1], down + pos[down][1]
        left_d, right_d = neg[left][0], pos[right][0]
        left, right = left + neg[left][1], right + pos[right][1]
    print(f'\nRow {r_index+1} and Column {c_index+1} finished')

def row_finish(grid, r_index, c_index, neg, pos, cross):
    '''When a row is complete, this places a cross on empty spaces'''
    i,j = r_index, c_index
    left, right = j,j
    left_d, right_d = False, False
    while (left_d & right_d) == False:
        grid[i][left] = cross[grid[i][left]]
        grid[i][right] = cross[grid[i][right]]
        left_d = neg[left][0]
        left = left + neg[left][1]
        right_d = pos[right][0]
        right = right + pos[right][1]
    print(f'\nRow {r_index+1} finished')

def column_finish(grid, r_index, c_index, neg, pos, cross):
    '''When a column is complete, this places a cross on empty spaces'''
    i,j = r_index, c_index
    up, down = i,i
    up_d, down_d = False, False
    while (up_d & down_d) == False:
        grid[up][j] = cross[grid[up][j]]
        grid[down][j] = cross[grid[down][j]]
        up_d = neg[up][0]
        up = up + neg[up][1]
        down_d = pos[down][0]
        down = down + pos[down][1]
    print(f'\nColumn {c_index+1} finished')

def task(check):
    '''returns the pattern of the boxes in the list'''
    count = 0
    l = []
    for index, i in enumerate(check):
        if i != 1:
            continue
        if i == 1:
            count += 1
            if index == len(check)-1:
                l.append(count)
                continue
        if check[index+1] != 1:
            l.append(count)
            count = 0
    return l

def row_complete(check, r_index, grid_check):
    '''Checks if pattern of boxes == row grid_check'''
    r = r_index
    if check == grid_check[r][0][0]:
        grid_check[r][0][1] = True
    else:
        grid_check[r][0][1] = False

def column_complete(check, c_index, grid_check):
    '''Checks if pattern of boxes == column grid_check'''
    c = c_index
    if check == grid_check[c][0][0]:
        grid_check[c][0][1] = True
    else:
        grid_check[c][0][1] = False

def row_check(r_index, c_index, grid):
    '''gets row from game, checks pattern, checks if complete then crosses spaces'''
    r, l = str(r_index+1), []
    for j in range(len(grid)):
        l.append(grid[r_index][j])
    row_complete(task(l), r, grid_check)
    return grid_check[r][0][1]

def column_check(r_index, c_index, grid):
    '''gets column from game, checks pattern, checks if complete then crosses spaces'''
    colconv = {'0': 'a', '1': 'b', '2': 'c', '3': 'd', '4': 'e', '5': 'f', '6': 'g', '7': 'h', '8': 'i', '9': 'j'}
    c, l = colconv[str(c_index)], []
    for i in range(len(grid)):
        l.append(grid[i][c_index])
    column_complete(task(l), c, grid_check)
    return grid_check[c][0][1]

def tiles_count(grid):
    count = 0
    for index in range(len(grid)):
        count += sum([1 for i in grid[index] if i==1])
    return count

def game_tile(grid):
    count = []
    for i in range(len(grid)):
        line = []
        for j in range(len(grid)):
            if grid[i][j] == 1:
                line.append(1)
                continue
            line.append(0)
        count.append(line)
    return np.array(count)

def input_action():
    '''Receives move and outputs the instruction'''
    values = input("r_index c_index action\t1-10\n")
    if ',' in values:
	    index = values.index(',')
	    a,b,c,d = (values[:index] + ' ' + values[index+1:]).split()
	    if index < 2: # r_range
		    r_index = int(a)-1
		    i_range = int(b)-1
		    c_index = int(c)-1
		    action = int(d)
		    return r_index, c_index, action, i_range, 0
	    else: #c_range
		    r_index = int(a)-1
		    c_index = int(b)-1
		    i_range = int(c)-1
		    action = int(d)
		    return r_index, c_index, action, i_range, 1
    a,b,c = tuple(values.split()) # Normal move
    return int(a)-1, int(b)-1, int(c), 0, 2

def input_response(a,b,c,d,e,grid): # a: r_index, b: c_index, c: action, d: range, e: instruction
    '''Effects instruction on the game board and outputs instruction for checking move and counting boxes'''
    if d > 9:
        d = 9
    if e == 1: # for c_range
        if list(grid[a][b:d+1]) == [c] * (d-b+1):
            grid[a][b:d+1] = [0] * (d-b+1)
        else:
            grid[a][b:d+1] = [c] * (d-b+1)
    elif e == 0: # for r_range
        for j in range(a, d+1):
            if grid[j][b] == c:
                grid[j][b] = 0
            else:
                grid[j][b] = c
    else: # normal move
        if grid[a][b] == c:
            grid[a][b] = 0
        else:
            grid[a][b] = c
    return a,b,d,e

def input_block(grid):
    '''Calls both input functions neatly'''
    a,b,c,d,e = input_action()
    return input_response(a,b,c,d,e,grid)

def check_block(a,b,d,e): # a: r_index, b: c_index, d: range, e: instruction
    '''Receives instruction for how to count boxes on the game board'''
    if e == 2: # normal move
        r_check, c_check = row_check(a, b, grid), column_check(a, b, grid)
        if r_check & c_check == True:
            finish(grid, a, b, conditions_neg, conditions_pos, cross)
        elif r_check == True:
            row_finish(grid, a, b, conditions_neg, conditions_pos, cross)
        elif c_check == True:
            column_finish(grid, a, b, conditions_neg, conditions_pos, cross)
    elif e == 0: # r_range: 1 column_check & multiple rows_check
        if column_check(a,b,grid) == True:
            column_finish(grid, a, b, conditions_neg, conditions_pos, cross)
        for r in range(b,d+1):
            if row_check(r, b, grid) == True:
                row_finish(grid, r, b, conditions_neg, conditions_pos, cross)
    elif e == 1: # c_range: multiple columns_check & 1 row_check
        if row_check(a, b, grid) == True:
            row_finish(grid, a, b, conditions_neg, conditions_pos, cross)
        for c in range(a,d+1):
            if column_check(a,c,grid) == True:
                column_finish(grid, a, c, conditions_neg, conditions_pos, cross)

def play(r_index, c_index, action, grid, grid_check, neg, pos, cross, tiles):
    '''Call to Start Game'''
    print("Game Loaded\nSTART!")
    print(f'\t0/63\n{grid}')
    while gameover(grid_check) == False:
        r_index, c_index, i_range, instruction = input_block(grid)
        tile_ingame = tiles_count(grid)
        if tiles == tile_ingame:
            if (game_tile(grid) == game_tile(solution())).all() == True:
                break
        check_block(r_index, c_index, i_range, instruction)
        print(f'\n\t{tile_ingame}/{tiles}')
        print(grid)
    print("\n\nYOU WON!\n\n*Playing Exit Animation*")

play(0, 0, 0, grid, grid_check, conditions_neg, conditions_pos, cross, tiles)
