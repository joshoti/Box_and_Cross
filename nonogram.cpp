#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <json/json.h>
#define NEWLINE cout << endl;
#define NEWLINE2 cout << "\n\n";
#define printGrid(x) printVec2(x)
#define CROSS_CELL(row,col) gameData.grid[row][col] = 5
#define CELL(row,col) gameData.grid[row][col]
#define LEVEL(x) x
#define CHAR(x) to_string(x)
#define ROWPattern(row) gridPattern[CHAR(row)][0]
#define ROWIsFilled(row) gridPattern[CHAR(row)][1]
#define COLPattern(col) gridPattern[colName[col]][0]
#define COLIsFilled(col) gridPattern[colName[col]][1]
using namespace std;

struct levelInfo {
	/*
	Holds all the info concerning the game
	
	Variables
		tiles:         number of tiles in the correct solution
		tileInGame:    number of tiles currently placed in game
		shape:         of grid (5x5, 10x10, 15x15)
		wideBase:	   if colPattern aligns with the grid
		colName:	   maps index to [string] letter
		gridPattern:   solution patterns for rows & columns
		grid:          the grid to be solved
		solutionGrid:  grid of the correct solution
		colPattern:    for displaying when print grid

	Methods
		extractColumnPattern:  to extract grid from gridPattern map
		Generate:              selects all info regarding a stage
	*/
	int tiles, tileInGame, shape;
	bool wideBase = false;
	unordered_map<int, string> colName = { {0,"a"}, {1,"b"}, {2,"c"}, {3,"d"}, {4,"e"},
										{5,"f"}, {6,"g"}, {7,"h"}, {8,"i"}, {9,"j"},
										{10,"k"}, {11,"l"}, {12,"m"}, {13,"n"}, {14,"o"} };
	Json::Value gridPattern;
	Json::Value grid;
	Json::Value solutionGrid;
	Json::Value colPattern;

	levelInfo(Json::Value levelParameters)
	{		
		tileInGame = 0;
		loadData(levelParameters);
	}
	void extractColumnPattern(Json::Value &columnPattern)
	{
		// Create empty grid of 0's for filling
		Json::Value dummyGrid;
		for (int r = 0; r < shape / 2; r++)
		{
			Json::Value row;
			for (int c = 0; c < shape; c++)
				row.append(0);
			dummyGrid.append(row);
		}

		// Writing rows [from gridPattern] to [the dummyGrid] columns
		int maxHeight = 0;
		for (int col = 0; col < shape; col++)
		{
			int row = 0;
			Json::Value column = COLPattern(col);
			//int size = ;
			for (auto element : column)
			{
				dummyGrid[row][col] = element;
				row++;

				// Checking if colPattern will align with grid
				if (!(wideBase) && element >= 10)
					wideBase = true;
			}		
			// To know the maxHeight of the grid
			if ((int)column.size() > maxHeight)
				maxHeight = column.size();
		}

		// Slicing the used ranges
		for (int rows = 0; rows < maxHeight; rows++)
			columnPattern.append(dummyGrid[rows]);
	}	
	void loadData(Json::Value &levelParameters)
	{			
		tiles = levelParameters["tiles"].asInt();
		shape = levelParameters["shape"].asInt();
		gridPattern = levelParameters["grid_check"];
		grid = levelParameters["grid"];
		solutionGrid = levelParameters["solutionGrid"];
		extractColumnPattern(colPattern);
	}
};
struct inputInfo {
	int row, col, endIndex, action, instruction;

	// Constructor
	inputInfo(string rawRow, string rawCol, string rawAction, string rawEndIndex, int rawInstruction)
	{
		row = stoi(rawRow) - 1;
		col = toascii(rawCol[0]) - 97;		
		action = stoi(rawAction);
		instruction = rawInstruction;
		if (instruction == 1) // Multiple Columns (horizontal)
			endIndex = toascii(rawEndIndex[0]) - 96; // (0-indexing)
		else // Multiple Rows (vertical)
			endIndex = stoi(rawEndIndex); // (0-indexing)
	}
};
void gameHelp()
{
	cout << "\n==============  HINT  ==============" << endl;
	cout << "Valid inputs are:                   R C A    OR  C R A       || ========  KEY  ========" << endl;
	cout << "1. One Cell:                       1 a 1     OR  a 1 1       ||   R - [single or multiple] Row" << endl;
	cout << "2. Multiple Rows (vertical):       1,3 a 1   OR  a 1,3 1     ||   C - [single or multiple] Column" << endl;
	cout << "3. Multiple Columns (horizontal):  1 a,c 1   OR  a,c 1 1     ||   A - Action" << endl;
}
void solutionHelp()
{
	cout << "\n===========  Solution Pattern Hint  ==========" << endl;
	cout << "Row solution pattern is on the right of the grid" << endl;
	cout << "Column solution pattern is on the bottom of the grid" << endl;
}
void inputHelp()
{
	cout << "\n\n=========  INPUT  =========" << endl;
	cout << "Input Hint? /  Need the Grid? / Need the solution pattern?" << endl;
	cout << "  press H   /     press G     /\t\tpress S" << endl;
}
vector<string> splitString(string sentence, string delimiter = " ")
{
	int start, end = -1 * delimiter.size();
	vector<string> words;
	do
	{
		start = end + delimiter.size();                       // Move start to location right after delimiter
		while (sentence[start] == delimiter[0])
			start++;
		end = sentence.find(delimiter, start);                // Find delimiter from start position
		words.push_back(sentence.substr(start, end - start)); // Append substring using start location and size of the subset (word) [end-start]
	} while (end != -1);
	return words;
}

void printSolution(levelInfo gameData, Json::Value Row, int rowName, int orientation, bool extraSpacing = false)
{
	string indent1 = " ", indent2 = "  ";
	if (extraSpacing)
	{
		indent1 = "  ";
		indent2 = "   ";
	}

	// Printing Values
	if (orientation) {

		// Printing Rows
		if (gameData.ROWIsFilled(rowName).asBool())
			cout << " []";
		else {
			cout << " [ ";
			for (auto element : Row)
			{
				if (element != 0) {
					if (element < 10)
						cout << element << indent1;
					else
						cout << element << " ";
				}
				else
					cout << indent2;
			}
			cout << "]";
		}
	}

	else {

		// Printing Columns
		unordered_map<int, string> &colName = gameData.colName;
		cout << " [ ";
		for (int col = 0; col < (int)Row.size(); col++) {
			if (Row[col] == 0 || gameData.COLIsFilled(col).asBool())
				cout << indent2;
			else {
				if (Row[col] < 10)
					cout << Row[col] << indent1;
				else
					cout << Row[col] << " ";
			}
		}
		cout << "]";
	}	
}

void printVec2(levelInfo gameData)
{
	string indent1 = "       ", indent2 = "    ", indent3 ="   ";

	// Display In-Game Info
	cout << "\n=========  " << gameData.tileInGame << "/" << gameData.tiles << "  =============" << endl;

	// Display Names of Columns (a-j) at the Top
	cout << indent1;
	for (int i = 0; i < gameData.shape; i++)
		cout << char(i + 97) << " ";
	NEWLINE2

	// Display game Grid
	int rowName = 1;
	for (auto row : gameData.grid)
	{
		// Display name of Row (1-10/15) on Left Hand
		if (rowName <= 9)
			cout << indent2 << rowName << "  ";
		else // row is 10
			cout << indent3 << rowName << "  ";

		// Display values in GRID
		for (auto element : row)
			cout << element << " "; 

		// Display name of Row (1-10/15) on Right Hand
		if (rowName <= 9)
			cout << " " << rowName << "  ";
		else // row is 10
			cout << " " << rowName << " ";

		// Display Row Solution Pattern
		printSolution(gameData, gameData.ROWPattern(rowName), rowName, 1);
		rowName++;
		NEWLINE
	}
	NEWLINE
	// Display Names of Columns (a-j) at the Top
	cout << indent1;
	for (int i = 0; i < gameData.shape; i++)
		cout << char(i + 97) << " ";
	NEWLINE

	// Display col names if not aligned
	if (gameData.wideBase) {
		NEWLINE
		cout << indent1;
		for (int i = 0; i < gameData.shape; i++)
			cout << char(i + 97) << "  ";
		NEWLINE
	}

	// Display Column Solution Pattern
	for (auto rowOfPatterns : gameData.colPattern)
	{
		cout << indent2;
		printSolution(gameData, rowOfPatterns, 0, 0, gameData.wideBase);
		NEWLINE
	}
}
void receiveRawInput(string raw, string &input) {
	cout << "\nRow(1-10) Col(a-j) Action (1,5,0)\t\tNeed help? Press 'I'" << endl;
	getline(cin, raw);

	// Changing to lowercase for uniformity
	for (auto element : raw)
		input += tolower(element);
}
inputInfo inputHandler(levelInfo &game)
{
	 // Using a loop in case of errors
	 while (true)
	 {
		 // Receiving raw input and change to lowercase
		 string raw, input;
		 receiveRawInput(raw, input);

		 while (input.size() < 5)
		 {
			 if (input == "i")
				 inputHelp();
			 else if (input == "h")
				 gameHelp();
			 else if (input == "g")
				 printGrid(game);
			 else if (input == "s")
				 solutionHelp();
			 receiveRawInput(raw, input = "");			 
		 }
		 int separator = input.find(',');
		 if (separator != input.npos) // Multiple Cells
		 {
			 input[separator] = ' ';
			 vector<string> parts = splitString(input);
			 // To catch Wrong Input
			 if (!(parts.size() == 4))
			 {
				 // Print the hint and retake input
				 gameHelp();
				 continue;
			 }

			 // Multiple Columns (horizontal)
			 if (isalpha(input[separator - 1]))
			 {
				 if (separator < 3) // Eg: a,c 1 1
				 {
					 inputInfo move(parts[2], parts[0], parts[3], parts[1], 1);
					 return move;
				 }
				 // else Eg: 1 a,c 1
				 inputInfo move(parts[0], parts[1], parts[3], parts[2], 1);
				 return move;
			 }
			 // Multiple Rows (vertical)
			 else
			 {
				 if (separator < 3) // Eg: 1,3 a 1
				 {
					 inputInfo move(parts[0], parts[2], parts[3], parts[1], 0);
					 return move;
				 }
				 // else  Eg: a 1,3 1
				 inputInfo move(parts[1], parts[0], parts[3], parts[2], 0);
				 return move;
			 }

		 }
		 else // One Cell
		 {
			 vector<string> parts = splitString(input);
			 // To catch Wrong Input
			 if (!(parts.size() == 3))
			 {
				 // Print the hint and retake input
				 gameHelp();
				 continue;
			 }

			 // Correct Input
			 if (isalpha(parts[0][0]))
			 { 
				 // 1st index is column Name. Eg: e 1 1				 				 
				 inputInfo move(parts[1], parts[0], parts[2], "0", 2);
				 return move;
			 }
			 // 1st index is row Name. Eg: 1 e 1
			 inputInfo move(parts[0], parts[1], parts[2], "0", 2);
			 return move;
		 }
	 }

}
void useMove(levelInfo &gameData, int row, int col, int action)
{
	 //if cell is 1, applying 1 will reduce tiles by 1			 
	 if (CELL(row,col) == 1 && action == 1)
	 {
		 CELL(row,col) = 0;
		 gameData.tileInGame--;
	 }

	 //if cell is 1, applying 5,0 will reduce tiles by 1
	 else if (CELL(row,col) == 1 && action != 1)
	 {
		 CELL(row,col) = action;
		 gameData.tileInGame--;
	 }

	 //if cell is 0,5 applying 1 will increase tiles by 1
	 else if (CELL(row,col) != 1 && action == 1)
	 {
		 CELL(row,col) = action;
		 gameData.tileInGame++;
	 }

	 //if cell is 0,5 applying 0,5 will have no change
	 else if (CELL(row,col) != 1 && action != 1)
		 CELL(row,col) = action;

}
 
Json::Value inGamePattern(Json::Value array)
{
	 /*
	 Returns the tile pattern of row/column in the game

	 Parameter
		array: row or column
	 */
	 int consecutiveCount = 0;
	 Json::Value tilePattern;
	 for (auto element : array)
	 {
		 if (element != 1)
		 {
			 if (consecutiveCount > 0)
			 {
				 tilePattern.append(consecutiveCount);
				 consecutiveCount = 0;
			 }
		 }
		 else
			 consecutiveCount++;
	 }
	 if (consecutiveCount > 0)
		 tilePattern.append(consecutiveCount);
	 return tilePattern;
}

bool rowCheck(levelInfo &gameData, int row, int col) 
{
	// Row in game to check
	Json::Value rowArray = gameData.grid[row];

	// if Pattern in Game == solutionPattern
	if (inGamePattern(rowArray) == gameData.ROWPattern(row + 1))
	{
		gameData.ROWIsFilled(row + 1) = true;
		return true;
	}
	gameData.ROWIsFilled(row + 1) = false;
	return false;
}
bool columnCheck(levelInfo &gameData, int row, int col)
{
	unordered_map<int, string> &colName = gameData.colName;

	// Col in game to check
	Json::Value colArray;
	for (int r = 0; r < gameData.shape; r++)
		colArray.append(CELL(r,col));

	// if Pattern in Game == solutionPattern
	if (inGamePattern(colArray) == gameData.COLPattern(col))
	{
		gameData.COLIsFilled(col) = true;
		return true;
	}
	gameData.COLIsFilled(col) = false;
	return false;
}
void rowFinish(levelInfo &gameData, int row, int col)
{
	int left = col, right = col + 1;
	while (left >= 0 || right < gameData.shape)
	{
		// Cross out empty spaces and Update horizontal markers
		if (left >= 0) {
			if (CELL(row, left) != 1)
				CROSS_CELL(row, left); // gameData.grid[row][left] = 5;
			left--;
		}
		if (right < gameData.shape) {			
			if (CELL(row, right) != 1)
				CROSS_CELL(row, right);
			right++;
		}
	}
	cout << "\nRow " << row + 1 << " finished!" << endl;
}
void columnFinish(levelInfo &gameData, int row, int col)
{
	int up = row, down = row + 1;
	while (up >= 0 || down < gameData.shape)
	{
		// Cross out empty spaces and Update vertical markers
		if (up >= 0) {
			if (CELL(up, col) != 1)
				CROSS_CELL(up, col); //	gameData.grid[up][col] = 5;
			up--;
		}
		if (down < gameData.shape) {
			if (CELL(down, col) != 1)
				CROSS_CELL(down, col);
			down++;
		}
	}
	cout << "\nColumn '" << char(col + 97) << "' finished!" << endl;
}
void finish(levelInfo &gameData, int row, int col)
{
	/*
	Runs rowFinish and columnFinish simultaneously
	*/
	int left = col, right = col + 1; // Horizontal markers
	int up = row, down = row + 1; // Vertical markers
	while (left >= 0 || right < gameData.shape || up >= 0 || down < gameData.shape)
	{
		// Cross out empty spaces and Update horizontal markers
		if (left >= 0) {
			if (CELL(row, left) != 1)
				CROSS_CELL(row, left);
			left--;
		}
		if (right < gameData.shape) {
			if (CELL(row, right) != 1)
				CROSS_CELL(row, right);
			right++;
		}

		// Cross out empty spaces and Update vertical markers
		if (up >= 0) {
			if (CELL(up, col) != 1)
				CROSS_CELL(up, col); 
			up--;
		}
		if (down < gameData.shape) {
			if (CELL(down, col) != 1)
				CROSS_CELL(down, col);
			down++;
		}
	}
	cout << "\nRow " << row + 1 << " and Column '" << char(col + 97) << "' finished!" << endl;
}

void gameHandler(levelInfo &gameData, inputInfo input) 
{
	/*
	Receives instruction for filling grid

	Sub Functions
		useMove:        Effects change on grid and updates in-game tile count
		inGamePattern:  Gets pattern from board. Basis for Check functions
		rowCheck:       Checks if row is solved
		columnCheck:    Checks if column is solved
		rowFinish:      Fills row whitespaces with a cross
		columnFinish:   Fills column whitespaces with a cross
		finish:         Fills row and column whitespaces with a cross, simultaneously
	*/

	// Effecting Change on Grid
	if (input.instruction == 0) // Multiple Rows (vertical)
	{
		for (int r = input.row; r < input.endIndex; r++)
			useMove(gameData, r, input.col, input.action);
	}
	else if (input.instruction == 1) // Multiple Columns (horizontal)
	{
		for (int c = input.col; c < input.endIndex; c++)
			useMove(gameData, input.row, c, input.action);
	}
	else // One Cell
		useMove(gameData, input.row, input.col, input.action);

	// Checks	
	if (input.instruction == 0) // Multiple Rows (vertical)
	{
		// One Column Check
		if (columnCheck(gameData, input.row, input.col))
			columnFinish(gameData, input.row, input.col);

		// Multiple Row Checks
		for (int r = input.row; r < input.endIndex; r++)
		{
			if (rowCheck(gameData, r, input.col))
				rowFinish(gameData, r, input.col);
		}
	}

	else if (input.instruction == 1) // Multiple Columns (horizontal)
	{
		// One Row Check
		if (rowCheck(gameData, input.row, input.col))
			rowFinish(gameData, input.row, input.col);	

		// Multiple Column Checks
		for (int c = input.col; c < input.endIndex; c++)
		{
			if (columnCheck(gameData, input.row, c))
				columnFinish(gameData, input.row, c);
		}
	}
	else // One Cell
	{
		bool rowIsComplete, colIsComplete;
		// Row and Column Check
		rowIsComplete = rowCheck(gameData, input.row, input.col);
		colIsComplete = columnCheck(gameData, input.row, input.col);

		if (rowIsComplete && colIsComplete)
			finish(gameData, input.row, input.col);

		else if (rowIsComplete)
			rowFinish(gameData, input.row, input.col);

		else if (colIsComplete)
			columnFinish(gameData, input.row, input.col);
	}
}

int playGame(int level)
{	
	ifstream data("src/nonogramstages.json", ifstream::binary);
	Json::Value levelData;
	data >> levelData;

	if (level < 1 || level > (int)levelData.size())
	{
		cout << "Select a level between 1-" << levelData.size() << "  ";
		cin >> level;
		while (!cin || level < 1 || level > (int)levelData.size())
		{
			cin.clear();
			cin.ignore(256, '\n');
			cout << "Select a level between 1-" << levelData.size() << "  ";
			cin >> level;
		}
	}
	cout << "\n\tHit Enter to Start game...";
	system("pause > 0");

	levelInfo game(levelData[to_string(level)]);
	printGrid(game);
	cin.ignore(256, '\n'); // To remove the 'select level' input
	while (game.tileInGame < game.tiles)
	{
		inputInfo move = inputHandler(game);
		gameHandler(game, move);
		printGrid(game);
	}
	return 1;
}
int main()
{
	int complete = playGame(LEVEL(-1)); // Select Level to play
	if (complete)
		cout << "\n\nYOU WON!";
}