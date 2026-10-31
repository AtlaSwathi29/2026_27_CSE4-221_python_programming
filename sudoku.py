"""
Case Study 6: Sudoku Validator and Solver
-----------------------------------------
Checks whether a 9x9 Sudoku board is valid (no repeated digit in any row,
column or 3x3 box; 0 means an empty cell) and solves it using backtracking.

Run:  python sudoku.py          -> solves the built-in sample puzzle
      python sudoku.py --demo   -> same, kept for consistency
"""
import sys

PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


def has_duplicates(group):
    """True if any digit 1-9 appears more than once in the list."""
    digits = [d for d in group if d != 0]      # ignore empty cells
    return len(digits) != len(set(digits))


def check_shape(board):
    """Board must be 9x9 with integers 0-9."""
    if len(board) != 9 or any(len(row) != 9 for row in board):
        raise ValueError("Board must be 9x9")
    for row in board:
        for value in row:
            if not isinstance(value, int) or value < 0 or value > 9:
                raise ValueError("Cells must be integers from 0 to 9")


def is_valid(board):
    """True if no row, column or 3x3 box contains a repeated digit."""
    check_shape(board)
    for i in range(9):
        row = board[i]
        column = [board[r][i] for r in range(9)]
        if has_duplicates(row) or has_duplicates(column):
            return False
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = [board[r][c]
                   for r in range(box_row, box_row + 3)
                   for c in range(box_col, box_col + 3)]
            if has_duplicates(box):
                return False
    return True


def is_complete(board):
    """True if the board is valid and has no empty cell."""
    return is_valid(board) and all(cell != 0 for row in board for cell in row)


def can_place(board, row, col, digit):
    """Check whether digit can go at (row, col) without breaking a rule."""
    if digit in board[row]:
        return False
    if digit in [board[r][col] for r in range(9)]:
        return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == digit:
                return False
    return True


def solve(board):
    """
    Backtracking solver. Fills the board in place and returns True if a
    solution exists, otherwise leaves the board unchanged and returns False.
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:                   # first empty cell
                for digit in range(1, 10):
                    if can_place(board, row, col, digit):
                        board[row][col] = digit        # try it
                        if solve(board):
                            return True
                        board[row][col] = 0            # undo (backtrack)
                return False                           # no digit fits here
    return True                                        # no empty cell left


def show(board):
    for r, row in enumerate(board):
        if r % 3 == 0 and r != 0:
            print("------+-------+------")
        parts = []
        for c, value in enumerate(row):
            if c % 3 == 0 and c != 0:
                parts.append("|")
            parts.append(str(value) if value else ".")
        print(" ".join(parts))


def demo():
    board = [row[:] for row in PUZZLE]      # copy so PUZZLE stays unchanged
    print("Puzzle:")
    show(board)
    print("\nPuzzle valid?", is_valid(board))
    if solve(board):
        print("\nSolution:")
        show(board)
        print("\nSolution valid and complete?", is_complete(board))
    else:
        print("No solution exists")


if __name__ == "__main__":
    demo()
