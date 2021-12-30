"""Nonogram's workings"""
import numpy as np
import random

conditions_pos = {0: [False,1], 1: [False,1], 2: [False,1] , 3: [False,1] , 4: [False,1] , 5: [False,1], 6: [False,1], 7: [False,1], 8: [False,1] , 9: [True,0]}
conditions_neg = {0: [True,0], 1: [False,-1], 2: [False,-1] , 3: [False,-1] , 4: [False,-1] , 5: [False,-1], 6: [False,-1], 7: [False,-1], 8: [False,-1] , 9: [False,-1]}
cross = {0: 5, 1: 1, 5:5}

grid = np.zeros((10,10))
grid_check = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], '1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], '10': []}
'''grid check value is a list that contains the row/column check and True value if completed'''
'''game ends when all grid_check[key][1] == True'''
def gameover(grid_check):
	for value in grid_check.values():
		if value[0][1] == False:
			break
		# q() Quit Game
		print("Game Quit")

"""NUMPY array functions"""
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
		# print(f'up {up}\tdown {down}\tleft {left}\tright {right}')

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
		# print(f'left {left}\tright {right}')

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
		# print(f'up {up}\tdown {down}')

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
		print("Ticked")
	else:
		grid_check[r][0][1] = False

def column_complete(check, c_index, grid_check):
	'''Checks if pattern of boxes == column grid_check'''
	c = c_index
	if check == grid_check[c][0][0]:
		grid_check[c][0][1] = True
		print("Ticked")
	else:
		grid_check[c][0][1] = False

def row_check(r_index, c_index, grid):
        '''gets row from game, checks pattern, checks if complete then crosses spaces'''
	r, l = str(r_index+1), []
	for j in range(len(grid)):
		l.append(int(grid[r_index][j]))
	res = task(l)
	# when sure of output, remove line above and return value to nothing or successful
	row_complete(res, r, grid_check)
	if grid_check[r][0][1] == True:
		row_finish(grid, r_index, c_index, conditions_neg, conditions_pos, cross)
	return res

def column_check(r_index, c_index, grid):
        '''gets column from game, checks pattern, checks if complete then crosses spaces'''
	colconv = {'0': 'a', '1': 'b', '2': 'c', '3': 'd', '4': 'e', '5': 'f', '6': 'g', '7': 'h', '8': 'i', '9': 'j'}
	c, l = colconv[str(c_index)], []
	for i in range(len(grid)):
		l.append(int(grid[i][c_index]))
	res = task(l)
	# when sure of output, remove line above and return value to nothing or successful
	column_complete(res, c, grid_check)
	if grid_check[c][0][1] == True:
		column_finish(grid, r_index, c_index, conditions_neg, conditions_pos, cross)
	return res

def target(index, condition, grid_check):
	'''Index a-j (columns) and 1-10 (rows)
	Condition is a list'''
	grid_check[index].append([condition, False])

def test(grid_check):
        '''creates conditions for all headers and prints it all out'''
	for key in grid_check.keys():
		target(key, [random.randint(1,3), random.randint(1,3), random.randint(1,4)], grid_check)
	print("Done creating test thingy")
	for k,v in grid_check.items():
		print(f'{k}: {v[0][0]}')
