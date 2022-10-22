""" Nonogram's workings """
import numpy as np

cross = {0: 5, 1: 1, 5:5}
def selectLevel1():
    """ Stage 56: Medium Difficulty for test """
    tiles = 63
    grid_check = {'a': [[2], False], 'b': [[1, 3, 1], False], 'c': [[7], False], 'd': [[1, 7], False], 'e': [[9], False], 'f': [[8], False], 'g': [[9], False], 'h': [[1, 7], False], 'i': [[1, 3, 1], False], 'j': [[1, 1], False],
              '1': [[3], False], '2': [[5], False], '3': [[3], False], '4': [[8], False], '5': [[6], False], '6': [[10], False], '7': [[9], False], '8': [[9], False], '9': [[3, 2], False], '10': [[3, 2], False]}
    grid = [[5,5,5,5,0,0,0,5,5,5], [0,0,5,0,0,0,0,0,5,0], [5,0,0,0,0,0,0,0,0,5],
            [0,0,0,0,0,0,0,0,0,5], [5,5,0,0,0,0,0,0,5,5], [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,5], [0,0,0,0,0,0,0,0,0,0], [5,5,0,0,0,0,0,0,0,0], [5,0,0,0,0,5,0,0,0,5]]
    solutionGrid = [[0,0,0,0,1,1,1,0,0,0], [0,0,0,1,1,1,1,1,0,0], [0,0,0,0,1,1,1,0,0,0], [0,1,1,1,1,1,1,1,1,0], [0,0,1,1,1,1,1,1,0,0],
                    [1,1,1,1,1,1,1,1,1,1], [1,1,1,1,1,1,1,1,1,0], [0,1,1,1,1,1,1,1,1,1], [0,0,1,1,1,0,1,1,0,0], [0,1,1,1,0,0,0,1,1,0]]
    return tiles, grid_check, np.resize(grid, (10,10)), solutionGrid

def selectLevel2():
    """ November 3 2021 Daily Challenge """
    tiles = 53
    grid_check = {'a': [[1], False], 'b': [[2,1], False], 'c': [[2,4], False], 'd': [[10], False], 'e': [[10], False], 'f': [[6], False], 'g': [[3,1,2], False], 'h': [[3,1,2], False], 'i': [[1,2], False], 'j': [[1,1], False],
                  '1': [[4,3], False], '2': [[5,2], False], '3': [[2,2], False], '4': [[5], False], '5': [[4], False], '6': [[7], False], '7': [[4], False], '8': [[6], False], '9': [[7], False], '10': [[2], False]}
    grid = [[5,0,0,0,0,5,5,0,0,0], [0,0,0,0,0,0,0,0,0,5], [5,0,0,0,0,5,0,0,0,5],
            [0,5,0,0,0,0,0,5,0,5], [5,5,0,0,0,0,0,0,5,5], [0,0,0,0,0,0,0,0,5,0],
            [0,5,0,0,0,0,0,0,5,0], [0,0,5,0,0,0,0,0,0,0], [5,5,0,0,0,0,0,0,0,0], [5,0,5,0,0,5,0,0,5,0]]
    solutionGrid = [[0,1,1,1,1,0,0,1,1,1], [1,1,1,1,1,0,1,1,0,0], [0,0,0,1,1,0,1,1,0,0], [0,0,1,1,1,1,1,0,0,0], [0,0,1,1,1,1,0,0,0,0],
                    [0,1,1,1,1,1,1,1,0,0], [0,0,1,1,1,1,0,0,0,0], [0,0,0,1,1,1,1,1,1,0], [0,0,0,1,1,1,1,1,1,1], [0,0,0,1,1,0,0,0,0,0]]
    return tiles, grid_check, np.resize(grid, (10,10)), solutionGrid

def selectLevel3():
    """ Frame """
    grid_check = {'a': [[], False], 'b': [[], False], 'c': [[], False], 'd': [[], False], 'e': [[], False], 'f': [[], False], 'g': [[], False], 'h': [[], False], 'i': [[], False], 'j': [[], False],
                  '1': [[], False], '2': [[], False], '3': [[], False], '4': [[], False], '5': [[], False], '6': [[], False], '7': [[], False], '8': [[], False], '9': [[], False], '10': [[], False]}

conditions_pos = {0: [False,1], 1: [False,1], 2: [False,1], 3: [False,1] , 4: [False,1] , 5: [False,1], 6: [False,1], 7: [False,1], 8: [False,1], 9: [True,0]}
conditions_neg = {0: [True,0], 1: [False,-1], 2: [False,-1], 3: [False,-1], 4: [False,-1], 5: [False,-1], 6: [False,-1], 7: [False,-1], 8: [False,-1], 9: [False,-1]}

def patternPuzzle():
    print("\n===========  Solution Pattern Hint  ==========")
    print("Row solution pattern is on the right of the grid")
    print("Column solution pattern is on the bottom of the grid")

def finish(grid, Row, Col, neg, pos, cross):
    """
    When a cell completes a row and column, this piece runs

    Parameters
        neg(dict): maps index to [bool, int] int: 0 or -1
        pos(dict): maps index to [bool, int] int: 0 or 1
        cross(dict): maps int to int

    Notes
        Left and Up use negative mapping
        Right and Down use positive mapping
        Both indices start from a cell and move outward to the edge
        Function completes when the last index arrives at the edge
        When index gets to the edge, the value stops changing
    """
    up, down, left, right = Row, Row, Col, Col
    up_Is_Done, down_Is_Done, left_Is_Done, right_Is_Done = False, False, False, False
    while (up_Is_Done & down_Is_Done & left_Is_Done & right_Is_Done) is False:
        # Cross out empty spaces
        grid[up][Col], grid[down][Col] = cross[grid[up][Col]], cross[grid[down][Col]]
        grid[Row][left], grid[Row][right] = cross[grid[Row][left]], cross[grid[Row][right]]

        # Update vertical markers
        up_Is_Done, down_Is_Done = neg[up][0], pos[down][0]
        up, down = up + neg[up][1], down + pos[down][1]

        # Update horizontal markers
        left_Is_Done, right_Is_Done = neg[left][0], pos[right][0]
        left, right = left + neg[left][1], right + pos[right][1]
    print(f'\nRow {Row+1} and Column {Col+1} finished')

def rowFinish(grid, Row, Col, neg, pos, cross):
    """
    When a row is complete, this places a cross on empty spaces
    """
    left, right = Col, Col
    left_Is_Done, right_Is_Done = False, False
    while (left_Is_Done & right_Is_Done) is False:
        # Cross out empty spaces
        grid[Row][left] = cross[grid[Row][left]]
        grid[Row][right] = cross[grid[Row][right]]

        # Update horizontal markers
        left_Is_Done, right_Is_Done = neg[left][0], pos[right][0]
        left, right = left + neg[left][1], right + pos[right][1]
    print(f'\nRow {Row+1} finished')

def columnFinish(grid, Row, Col, neg, pos, cross):
    """
    When a column is complete, this places a cross on empty spaces
    """
    up, down = Row, Row
    up_Is_Done, down_Is_Done = False, False
    while (up_Is_Done & down_Is_Done) is False:
        # Cross out empty spaces
        grid[up][Col] = cross[grid[up][Col]]
        grid[down][Col] = cross[grid[down][Col]]

        # Update vertical markers
        up_Is_Done, down_Is_Done = neg[up][0], pos[down][0]
        up, down = up + neg[up][1], down + pos[down][1]
    print(f'\nColumn {Col+1} finished')

def task(array):
    """
    Returns the pattern of the boxes in the list

    Parameter
        array(list): could be a row or column

    Example Use
        >>> grid = [[0,1,1,0],
                    [1,0,0,1]]
        >>> task(grid[0])
        [2]    # Two adjacent 1-cells in first row

        >>> task(grid[1])
        [1,1]  # Two 1-cells separated by space

        >>> task(grid.column('a'))
        [1]    # One 1-cell beside One 0-cell
    """
    consecutiveCount = 0
    patternArray = []
    for index, cell in enumerate(array):
        if cell != 1:
            continue
        if cell == 1:
            consecutiveCount += 1
            if index == len(array)-1:
                patternArray.append(consecutiveCount)
                continue
        if array[index+1] != 1:
            patternArray.append(consecutiveCount)
            consecutiveCount = 0
    return patternArray

def rowComplete(check, rowName, grid_check):
    """
    Checks if pattern of boxes == row grid_check
    
    rowName (1 - 10)
    """
    if check == grid_check[rowName][0]:
        grid_check[rowName][1] = True
    else:
        grid_check[rowName][1] = False

def columnComplete(check, colName, grid_check):
    """
    Checks if pattern of boxes == column grid_check

    colName (a - j)
    """
    if check == grid_check[colName][0]:
        grid_check[colName][1] = True
    else:
        grid_check[colName][1] = False

def rowCheck(rowIndex, columnIndex, grid):
    """
    Gets row from game, checks pattern, checks if complete then crosses spaces

    Explanation
        rowIndex = 0
        rowName = '1'
    """
    rowName = str(rowIndex+1)
    rowArray = grid[rowIndex]
    rowComplete(task(rowArray), rowName, grid_check)
    return grid_check[rowName][1]

def columnCheck(rowIndex, columnIndex, grid):
    """
    Gets column from game, checks pattern, checks if complete then crosses spaces

    Explanation
        >>> chr(97)
        'a'

        >>> ord('a')
        97

        colIndex = 0
        colName = 'a'

        colIndex = 9
        colName = 'j'
    """    
    colName, columnArray = chr(columnIndex + 97), []
    for r in range(len(grid)):
        columnArray.append(grid[r][columnIndex])
    columnComplete(task(columnArray), colName, grid_check)
    return grid_check[colName][1]

def game_tile(grid):
    """
    Counts tiles on game board & gets arrangement of boxes on board

    Example Use
        >>> grid = [[5,1,1,5],
                    [1,5,5,1]]
        >>> game_tile(grid)
        [[0,1,1,0], [1,0,0,1]], 4
    """
    gridPattern = []
    tile_sum = 0
    for row in range(len(grid)):
        rowPattern = []
        tile_sum += sum([1 for cell in grid[row] if cell==1])
        for col in range(len(grid[0])):
            if grid[row][col] == 1:
                rowPattern.append(1)
                continue
            rowPattern.append(0)
        gridPattern.append(rowPattern)
    return np.array(gridPattern), tile_sum

def gameHelp():
    print("\n==============  HINT  ==============")
    print("Valid inputs are:")
    print("1 a 1    # One Cell")
    print("1,3 a 1  # Multiple Rows    (vertical)")
    print("1 a,c 1  # Multiple Columns (horizontal)")

def printGrid(tileInGame, colPattern):
    """
    Prints
        The number of tiles filled in game
        The names of the rows (digits) and columns (letters) to the top and left of the grid
        The row and column solution patterns on the bottom and right of the grid
    """
    print(f"\n=========  {tileInGame}/{tiles}  =============")
    print('    a b c d e f g h i j') # Column Name
    for r in range(len(grid)):
        print(f"{r+1: >2} {grid[r]} {grid_check[str(r+1)][0]}") # Row-name  Grid-row  Row-solution-pattern
    print()
    for r in range(len(colPattern)):
        print(f"{'':>2} {colPattern[r]}") # Column-solution-pattern

def columnPattern(grid_check):
    gridpattern = [[0]*10 for i in range(7)]
    maxHeight = 0
    for colIndex, colName in enumerate(range(97,107)):
        listModel = grid_check[chr(colName)][0]
        maxHeight = max(maxHeight, len(listModel))
        for row in range(len(listModel)):
                gridpattern[row][colIndex] = listModel[row]
    return gridpattern[:maxHeight]
    
def input_action():
    """
    Receives move and outputs the instruction

    Example Use
        >>> Row(1-10)  Col(a-j)  Action(1,5,0) # One cell move
        1 a 1     # User Input
        returns (0, 0, 1, 0, 2)
        Translation: Apply 1 to Row 1 column a

        >>> Row(1-10)  Col(1-10)  Action(1,5,0) # Multiple row move
        1,3 a 1   # User Input
        returns (0, 0, 1, 2, 0)
        Translation: Apply 1 to Row 1-3 on column a

        >>> Row(1-10)  Col(1-10)  Action(1,5,0) # Multiple column move
        1 a,c 1   # User Input
        returns (0, 0, 1, 2, 1)
        Translation: Apply 1 to Column a-c on row 1

    Returns
        row(int) Row of cell(s) on grid
        col(int) Col of cell(s) on grid
        action(int) (1 -> add block, 0 -> empty, 5 -> cross)
        endIndex(int) End range of adjacent cell(s) to act on
        instruction(int) (0 -> Multiple rows, 1 -> Multiple columns, 2 -> One Cell)
    """
    patternPuzzle()
    while True:
        print("\n\n=========  INPUT  =========")
        print("Input Hint? /  Need the Grid? / Need the solution pattern?")
        print("  press H   /     press G     /\t\tpress P\n")
        values = input("Row(1-10)  Col(a-j)  Action(1,5,0)\n>>> Your Input:  ")
        if values.lower() == 'h':
            gameHelp()
        elif values.lower() == 'g':
            printGrid(game_tile(grid)[1], colSolutionPattern)
        elif values.lower() == 'p':
            patternPuzzle()
        else:
            break
    if ',' in values:
        separator = values.index(',')
        a, b, c, d = (values[:separator] + ' ' + values[separator+1:]).split()
        if separator < 3: # Multiple rows (vertical)
            rowStartIndex = int(a)-1
            rowEndIndex = int(b)-1
            columnIndex = ord(c)-97
            action = int(d)
            return rowStartIndex, columnIndex, action, rowEndIndex, 0
        else: # Multiple columns (horizontal)
            rowIndex = int(a)-1
            columnStartIndex = ord(b)-97
            columnEndIndex = ord(c)-97
            action = int(d)
            return rowIndex, columnStartIndex, action, columnEndIndex, 1
    rowIndex, columnIndex, action = values.split() # One Cell
    return int(rowIndex)-1, ord(columnIndex)-97, int(action), 0, 2

def input_response(Row, Col, action, EndIndex, Instruction, grid):
    """
    Effects instruction on the game board and outputs instruction for checking move and counting boxes
    """
    if EndIndex > 9:
        EndIndex = 9
    if Instruction == 1: # Multiple columns (horizontal)
        if list(grid[Row][Col:EndIndex+1]) == [action] * (EndIndex-Col+1):
            grid[Row][Col:EndIndex+1] = [0] * (EndIndex-Col+1)
        else:
            grid[Row][Col:EndIndex+1] = [action] * (EndIndex-Col+1)
    elif Instruction == 0: # Multiple rows (vertical)
        for r in range(Row, EndIndex+1):
            if grid[r][Col] == action:
                grid[r][Col] = 0
            else:
                grid[r][Col] = action
    else: # One cell
        if grid[Row][Col] == action:
            grid[Row][Col] = 0
        else:
            grid[Row][Col] = action
    return Row, Col, EndIndex, Instruction

def input_block(grid):
    """
    Calls both input functions neatly

    inputAction   takes the input information and formats into instruction
    inputResponse takes the instruction and executes on grid
    """
    rowIndex, columnIndex, action, endIndex, instruction = input_action()
    return input_response(rowIndex, columnIndex, action, endIndex, instruction, grid)

def check_block(row, col, endIndex, instruction):
    """
    Receives instruction for how to count boxes on the game board

    Logic
        If One Cell was acted on, we check 1 row and 1 column
        If Multiple Rows were acted on, we check 1 column and multiple rows
        If Multiple Columns were acted on, we check 1 row and multiple columns

    Essence
        RowFinish/ColumnFinish means to cover empty boxes with crosses on the row/col
    """
    if instruction == 2: # One Cell
        # Row and Column Check
        row_Is_Complete = rowCheck(row, col, grid)
        col_Is_Complete = columnCheck(row, col, grid)

        # Complete? Finish
        if row_Is_Complete and col_Is_Complete:
            finish(grid, row, col, conditions_neg, conditions_pos, cross)
        elif row_Is_Complete:
            rowFinish(grid, row, col, conditions_neg, conditions_pos, cross)
        elif col_Is_Complete:
            columnFinish(grid, row, col, conditions_neg, conditions_pos, cross)
            
    elif instruction == 0: # Multiple Rows (vertical)
        # 1 Column Check
        if columnCheck(row, col, grid):
            columnFinish(grid, row, col, conditions_neg, conditions_pos, cross)

        # Multiple Row Checks
        for r in range(row, endIndex+1):
            if rowCheck(r, col, grid):
                rowFinish(grid, r, col, conditions_neg, conditions_pos, cross)
                
    elif instruction == 1: # Multiple Columns (horizontal)
        # 1 Row Check
        if rowCheck(row, col, grid):
            rowFinish(grid, row, col, conditions_neg, conditions_pos, cross)

        # Multiple Column Checks
        for c in range(col, endIndex+1):
            if columnCheck(row, c, grid):
                columnFinish(grid, row, c, conditions_neg, conditions_pos, cross)
        
def play(grid, grid_check, neg, pos, cross, tiles, solution):
    """ Call to Start Game """
    gameHelp()
    printGrid(0, colSolutionPattern)
    while True:
        rowIndex, colIndex, EndIndex, instruction = input_block(grid)
        tile_ingame = game_tile(grid)
        if tiles == tile_ingame[1]:
            if (tile_ingame[0] == solution).all(): # Puzzle solved
                break
        check_block(rowIndex, colIndex, EndIndex, instruction)
        printGrid(tile_ingame[1], colSolutionPattern)
    print("\n\nYOU WON!\n\n*Playing Exit Animation*")

tiles, grid_check, grid, solution = selectLevel1()
colSolutionPattern = np.array(columnPattern(grid_check))
play(grid, grid_check, conditions_neg, conditions_pos, cross, tiles, solution)
