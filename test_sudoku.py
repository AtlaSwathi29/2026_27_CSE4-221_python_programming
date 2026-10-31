"""Test cases for Case Study 6 (Sudoku Validator and Solver).
Run:  python test_sudoku.py           -> readable results
      python test_sudoku.py --table   -> Markdown table for the report
"""
import sys
from sudoku import PUZZLE, is_complete, is_valid, solve

SOLUTION = ["534678912", "672195348", "198342567",
            "859761423", "426853791", "713924856",
            "961537284", "287419635", "345286179"]


def run_cases(cases):
    """Each case is (description, expected, function). Errors become 'Error: message'."""
    rows, failed = [], 0
    for number, (description, expected, func) in enumerate(cases, start=1):
        try:
            actual = func()
        except Exception as err:
            actual = "Error: " + str(err)
        passed = actual == expected
        failed += not passed
        rows.append((f"TC{number:02d}", description, expected, actual,
                     "PASS" if passed else "FAIL"))
    if "--table" in sys.argv:
        print("| TC | Scenario / Input | Expected Output | Actual Output | Result |")
        print("|----|------------------|-----------------|---------------|--------|")
        for tc, d, e, a, r in rows:
            print(f"| {tc} | {d} | `{str(e)}` | `{str(a)}` | {r} |")
    else:
        for tc, d, e, a, r in rows:
            print(f"{tc} {r}  {d}\n      expected={e!r}  actual={a!r}")
    print(f"\n{len(rows) - failed}/{len(rows)} test cases passed")
    return failed == 0


def copy():
    return [row[:] for row in PUZZLE]


def with_change(row, col, value):
    board = copy()
    board[row][col] = value
    return is_valid(board)


def solved_as_text():
    board = copy()
    solve(board)
    return ["".join(str(d) for d in row) for row in board]


def solved_is_complete():
    board = copy()
    solve(board)
    return is_complete(board)


def unsolvable():
    # Row 0 needs a 9 in its last cell, but column 8 already has a 9.
    board = [[1, 2, 3, 4, 5, 6, 7, 8, 0]] + [[0] * 9 for _ in range(8)]
    board[1][8] = 9
    before = [row[:] for row in board]
    return (is_valid(board), solve(board), board == before)


def empty_board():
    board = [[0] * 9 for _ in range(9)]
    return (solve(board), is_complete(board))


CASES = [
    ("Sample puzzle (partly filled) is valid", True, lambda: is_valid(PUZZLE)),
    ("Duplicate 7 in a row only (put 7 at row 1, col 9)", False,
     lambda: with_change(0, 8, 7)),
    ("Duplicate 3 in a column only (put 3 at row 9, col 2)", False,
     lambda: with_change(8, 1, 3)),
    ("Duplicate 9 in a 3x3 box only (put 9 at row 1, col 3)", False,
     lambda: with_change(0, 2, 9)),
    ("Legal extra digit (put 4 at row 1, col 3)", True,
     lambda: with_change(0, 2, 4)),
    ("Board with only 8 rows", "Error: Board must be 9x9", lambda: is_valid(PUZZLE[:8])),
    ("Cell containing 10", "Error: Cells must be integers from 0 to 9",
     lambda: with_change(0, 2, 10)),
    ("Unsolved puzzle is not complete", False, lambda: is_complete(PUZZLE)),
    ("Solver returns True for the sample puzzle", True, lambda: solve(copy())),
    ("Solved grid equals the known solution", SOLUTION, solved_as_text),
    ("Solved grid is valid and complete", True, solved_is_complete),
    ("Unsolvable board: (valid?, solved?, board unchanged?)", (True, False, True),
     unsolvable),
    ("Empty board: (solved?, complete?)", (True, True), empty_board),
]

if __name__ == "__main__":
    sys.exit(0 if run_cases(CASES) else 1)
