"""Test cases for Case Study 7 (Tic-Tac-Toe with Minimax AI).
Run:  python test_tictactoe_ai.py           -> readable results
      python test_tictactoe_ai.py --table   -> Markdown table for the report
"""
import sys
from tictactoe_ai import best_move, empty_cells, other, winner


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


def b(text):
    """Make a board from a 9-character string; '.' means empty."""
    return [" " if ch == "." else ch for ch in text]


def never_loses(ai):
    """
    Try EVERY possible move of the human against the AI and confirm that
    the human never wins. Returns True if the AI never loses.
    """
    human = other(ai)

    def explore(board, turn):
        result = winner(board)
        if result == human:
            return False
        if result is not None:
            return True
        if turn == ai:
            cell = best_move(board, ai)
            board[cell] = ai
            ok = explore(board, human)
            board[cell] = " "
            return ok
        for cell in empty_cells(board):
            board[cell] = human
            ok = explore(board, ai)
            board[cell] = " "
            if not ok:
                return False
        return True

    return explore([" "] * 9, "X")


CASES = [
    ("Winner: top row of X", "X", lambda: winner(b("XXX......"))),
    ("Winner: left column of O", "O", lambda: winner(b("O..O..O.."))),
    ("Winner: main diagonal of X", "X", lambda: winner(b("X...X...X"))),
    ("Winner: anti-diagonal of O", "O", lambda: winner(b("..O.O.O.."))),
    ("Full board, no line -> Draw", "Draw", lambda: winner(b("XOXXOOOXX"))),
    ("Last move completes a line on a full board", "X",
     lambda: winner(b("XOXOXOOXX"))),
    ("Game still in progress", None, lambda: winner(b("XO......."))),
    ("AI (X) completes its own line: X X . / O O .", 2,
     lambda: best_move(b("XX.OO...."), "X")),
    ("AI (O) blocks X's line: X X . / . O .", 2,
     lambda: best_move(b("XX..O...."), "O")),
    ("AI (O) answers corner opening with the centre", 4,
     lambda: best_move(b("X........"), "O")),
    ("AI moves first on empty board -> centre", 4,
     lambda: best_move(b("........."), "X")),
    ("AI as O can never lose (human tries every move)", True, lambda: never_loses("O")),
    ("AI as X can never lose (human tries every move)", True, lambda: never_loses("X")),
]

if __name__ == "__main__":
    sys.exit(0 if run_cases(CASES) else 1)
