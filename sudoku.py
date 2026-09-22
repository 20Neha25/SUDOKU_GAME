import random


# Check whether a number can be placed in a cell
def is_valid(board, row, col, num):

    # Check row
    for j in range(9):
        if board[row][j] == num:
            return False

    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Find the starting position of the 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    # Check 3x3 box
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True


# Find an empty cell
def find_empty(board):

    for row in range(9):
        for col in range(9):

            if board[row][col] == 0:
                return row, col

    return None


# Solve Sudoku using backtracking
def solve(board):

    empty = find_empty(board)

    # If there is no empty cell, Sudoku is solved
    if empty is None:
        return True

    row, col = empty

    numbers = list(range(1, 10))

    random.shuffle(numbers)

    for num in numbers:

        # Check whether the number satisfies the constraints
        if is_valid(board, row, col, num):

            # Place the number
            board[row][col] = num

            # Continue solving
            if solve(board):
                return True

            # Backtrack
            board[row][col] = 0

    return False


# Generate a complete Sudoku solution
def generate_solution():

    board = [[0 for _ in range(9)] for _ in range(9)]

    solve(board)

    return board


# Generate a playable Sudoku puzzle
def generate_puzzle(difficulty="Medium"):

    solution = generate_solution()

    # Copy the solution
    puzzle = [row[:] for row in solution]

    # Decide how many cells to remove
    if difficulty == "Easy":
        cells_to_remove = 35

    elif difficulty == "Medium":
        cells_to_remove = 45

    else:
        cells_to_remove = 55

    # Create a list of all cell positions
    positions = [
        (row, col)
        for row in range(9)
        for col in range(9)
    ]

    # Randomize positions
    random.shuffle(positions)

    # Remove numbers
    for row, col in positions[:cells_to_remove]:
        puzzle[row][col] = 0

    return puzzle, solution


# Check the player's completed board
def check_board(board, solution):

    for row in range(9):
        for col in range(9):

            # Empty cell means the puzzle is incomplete
            if board[row][col] == 0:
                return False

            # Wrong number
            if board[row][col] != solution[row][col]:
                return False

    return True