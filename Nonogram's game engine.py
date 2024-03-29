""" Nonogram's workings """
import numpy as np

def loadData():
    """
    Creates the database
    """
    import sqlite3
    with open (r'C:\Users\Joshua\Documents\nonogramstage.sql') as file:
        sqlfile = file.read()
    SQLconnector = sqlite3.connect(r'C:\Users\Joshua\Documents\leveldatabase.db')
    cursor = SQLconnector.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS level;")
    for command in sqlfile.split(';'):
        cursor.execute(command)
    return cursor

def loadLevel(number, cursor):
    """
    Queries the database
    """
    while (number <= 0) or  (number > cursor.lastrowid):
        number = int(input(f"Select another number between 1-{cursor.lastrowid}  "))
    import json
    levelJSON = cursor.execute(f"select information from level where id = {number};")    
    return json.loads(levelJSON.fetchone()[0])

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
    print(f'\nRow "{Row+1}" and Column "{chr(Col+97)}" Finished!')

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
    print(f'\nRow "{Row+1}" Finished!')

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
    print(f'\nColumn "{chr(Col+97)}" Finished!')

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
    rowComplete(task(rowArray), rowName, gamedata['grid_check'])
    return gamedata['grid_check'][rowName][1]

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
    columnComplete(task(columnArray), colName, gamedata['grid_check'])
    return gamedata['grid_check'][colName][1]

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
    print("One Cell:                       1 a 1     OR  a 1 1")
    print("Multiple Rows (vertical):       1,3 a 1   OR  a 1,3 1")
    print("Multiple Columns (horizontal):  1 a,c 1   OR  a,c 1 1")

def printGrid(tileInGame, colPattern, wideColBase):
    """
    Prints
        The number of tiles filled in game
        The names of the rows (digits) and columns (letters) to the top and left of the grid
        The row and column solution patterns on the bottom and right of the grid
    """
    print(f"\n=========  {tileInGame}/{gamedata['tiles']}  =============")
    print('    a b c d e f g h i j') # Column Name
    for r in range(len(gamedata['grid'])):
        #       Row-name         Grid-row              Row-solution-pattern
        print(f"{r+1: >2} {gamedata['grid'][r]}  {gamedata['grid_check'][str(r+1)][0]}")
    print()

    if wideColBase:
        print("".ljust(3), end="")
        for i in range(gamedata['shape']):
            print(chr(i+97), end="  ")
        print()
        print(colPattern)
    else:
        # Column-solution-pattern
        for r in range(len(colPattern)):            
            print(f"{'': >2} {colPattern[r]}") # :>2 controls the right indent level"""

def columnPattern(grid_check):
    """
    Variable
        gamedata['shape']:   can be 5x5, 10x10, or 15x15
    """
    gridpattern = [[0]*gamedata['shape'] for i in range(gamedata['shape']//2)]
    maxHeight = 0
    wideColBase = False
    for col in range(gamedata['shape']):
        listModel = grid_check[chr(col+97)][0]
        maxHeight = max(maxHeight, len(listModel))
        for row in range(len(listModel)):
                gridpattern[row][col] = listModel[row]
                if not(wideColBase) and listModel[row] >= 10:
                    wideColBase = True                    
    return gridpattern[:maxHeight], wideColBase
    
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
    while True:         
        values = input("\n\nRow(1-10)  Col(a-j)  Action(1,5,0)\t[ Need Help? Press O ]\n>>> Your Input:  ")
        if values.lower() == 'h':
            gameHelp()
        elif values.lower() == 'g':
            printGrid(game_tile(gamedata['grid'])[1], colSolutionPattern, wideColBase)
        elif values.lower() == 'p':
            patternPuzzle()
        elif values.lower() == 'o':
            print("\n\n=========  INPUT  =========")
            print("Input Hint? /  Need the Grid? / Need the solution pattern?")
            print("  press H   /     press G     /\t\tpress P")
        elif len(values) < 5:
            print("Input not recognised")
            continue
        else:
            break
    if ',' in values:
        separator = values.index(',')
        a, b, c, d = (values[:separator] + ' ' + values[separator+1:]).split()
        action = int(d)
        
        # Multiple rows (vertical)
        if values[separator-1].isnumeric(): 
            if separator < 3: # Eg: 1,3 a 1
                rowStartIndex = int(a)-1 
                rowEndIndex = int(b)-1
                columnIndex = ord(c)-97                
            else: # Eg: a 1,3 1
                columnIndex = ord(a)-97
                rowStartIndex = int(b)-1
                rowEndIndex = int(c)-1
            return rowStartIndex, columnIndex, action, rowEndIndex, 0

        # Multiple columns (horizontal)
        else: 
            if separator < 3: # Eg: a,c 1 1
                columnStartIndex = ord(a)-97
                columnEndIndex = ord(b)-97
                rowIndex = int(c)-1
            else: # Eg: 1 a,c 1
                rowIndex = int(a)-1
                columnStartIndex = ord(b)-97
                columnEndIndex = ord(c)-97
            return rowIndex, columnStartIndex, action, columnEndIndex, 1
        
    # One Cell
    rowIndex, columnIndex, action = values.split() 
    if rowIndex.isalpha(): # rowIndex is colName. Eg: e 1 1
        return int(columnIndex)-1, ord(rowIndex)-97, int(action), 0, 2
    return int(rowIndex)-1, ord(columnIndex)-97, int(action), 0, 2 # rowIndex is rowName. Eg: 1 e 1

def input_response(Row, Col, action, EndIndex, Instruction, grid):
    """
    Effects instruction on the game board and outputs instruction for checking move and counting boxes
    """    
    if EndIndex > gamedata['shape']-1:
        EndIndex = gamedata['shape']-1
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
        row_Is_Complete = rowCheck(row, col, gamedata['grid'])
        col_Is_Complete = columnCheck(row, col, gamedata['grid'])

        # Complete? Finish
        if row_Is_Complete and col_Is_Complete:
            finish(gamedata['grid'], row, col, conditions_neg, conditions_pos, cross)
        elif row_Is_Complete:
            rowFinish(gamedata['grid'], row, col, conditions_neg, conditions_pos, cross)
        elif col_Is_Complete:
            columnFinish(gamedata['grid'], row, col, conditions_neg, conditions_pos, cross)
            
    elif instruction == 0: # Multiple Rows (vertical)
        # 1 Column Check
        if columnCheck(row, col, gamedata['grid']):
            columnFinish(gamedata['grid'], row, col, conditions_neg, conditions_pos, cross)

        # Multiple Row Checks
        for r in range(row, endIndex+1):
            if rowCheck(r, col, gamedata['grid']):
                rowFinish(gamedata['grid'], r, col, conditions_neg, conditions_pos, cross)
                
    elif instruction == 1: # Multiple Columns (horizontal)
        # 1 Row Check
        if rowCheck(row, col, gamedata['grid']):
            rowFinish(gamedata['grid'], row, col, conditions_neg, conditions_pos, cross)

        # Multiple Column Checks
        for c in range(col, endIndex+1):
            if columnCheck(row, c, gamedata['grid']):
                columnFinish(gamedata['grid'], row, c, conditions_neg, conditions_pos, cross)
        
def play(gamedata, neg, pos, cross):    
    """
    Call to Start Game
    """
    gameHelp()    
    patternPuzzle()
    input("\nHit Enter to Start")
    printGrid(0, colSolutionPattern, wideColBase)
    while True:
        rowIndex, colIndex, EndIndex, instruction = input_block(gamedata['grid'])
        tile_ingame = game_tile(gamedata['grid'])
        if gamedata['tiles'] == tile_ingame[1]:            
            if (tile_ingame[0] == gamedata['solutionGrid']).all():
                # Puzzle solved
                break
        check_block(rowIndex, colIndex, EndIndex, instruction)
        printGrid(tile_ingame[1], colSolutionPattern, wideColBase)
    print("\n\nYOU WON!\n\n*Playing Exit Animation*")

# Variables
cross = {0: 5, 1: 1, 5:5}
conditions_pos = {0: [False,1], 1: [False,1], 2: [False,1], 3: [False,1] , 4: [False,1] , 5: [False,1], 6: [False,1], 7: [False,1], 8: [False,1], 9: [True,0]}
conditions_neg = {0: [True,0], 1: [False,-1], 2: [False,-1], 3: [False,-1], 4: [False,-1], 5: [False,-1], 6: [False,-1], 7: [False,-1], 8: [False,-1], 9: [False,-1]}

# Read database
cursor = loadData()

# User input to query database
number = int(input(f"Select a number between 1-{cursor.lastrowid}  "))
gamedata = loadLevel(number, cursor)

# Change to numpy array for display purposes
gamedata['grid'] = np.array(gamedata['grid'])

# Extract pattern and determine display style
columnGrid, wideColBase = columnPattern(gamedata['grid_check'])
colSolutionPattern = np.array(columnGrid)

# Begin
play(gamedata, conditions_neg, conditions_pos, cross)
