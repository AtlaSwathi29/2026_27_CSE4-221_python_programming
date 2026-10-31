"""Test cases for Case Study 8 (Matrix Operations Toolkit).
Run:  python test_matrix_toolkit.py           -> readable results
      python test_matrix_toolkit.py --table   -> Markdown table for the report
"""
import sys
from matrix_toolkit import (add, determinant, inverse, is_symmetric, multiply,
                            subtract, trace, transpose)


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


A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
C = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
SINGULAR_3X3 = [[2, 0, 1], [1, 3, 2], [1, 1, 1]]
D4 = [[1, 0, 2, -1], [3, 0, 0, 5], [2, 1, 4, -3], [1, 0, 5, 0]]


def c_times_inverse():
    product = multiply(C, inverse(C))
    return [[round(v, 4) + 0 for v in row] for row in product]


CASES = [
    ("A + B  (A=[[1,2],[3,4]], B=[[5,6],[7,8]])", [[6, 8], [10, 12]], lambda: add(A, B)),
    ("A - B", [[-4, -4], [-4, -4]], lambda: subtract(A, B)),
    ("A x B", [[19, 22], [43, 50]], lambda: multiply(A, B)),
    ("Transpose of 2x3 [[1,2,3],[4,5,6]]", [[1, 4], [2, 5], [3, 6]],
     lambda: transpose([[1, 2, 3], [4, 5, 6]])),
    ("Add 2x2 and 2x3", "Error: Matrices must have the same size to add",
     lambda: add(A, [[1, 2, 3], [4, 5, 6]])),
    ("Multiply 2x2 by 3x2 (sizes do not match)",
     "Error: Columns of A must equal rows of B",
     lambda: multiply(A, [[1, 2], [3, 4], [5, 6]])),
    ("Multiply 2x3 by 3x1 -> 2x1", [[14], [32]],
     lambda: multiply([[1, 2, 3], [4, 5, 6]], [[1], [2], [3]])),
    ("Determinant of [[4,7],[2,6]]", 10, lambda: determinant([[4, 7], [2, 6]])),
    ("Determinant of 3x3 C", 1, lambda: determinant(C)),
    ("Determinant of singular 3x3", 0, lambda: determinant(SINGULAR_3X3)),
    ("Determinant of 4x4 matrix", 30, lambda: determinant(D4)),
    ("Determinant of a non-square matrix", "Error: Matrix must be square",
     lambda: determinant([[1, 2, 3], [4, 5, 6]])),
    ("Inverse of [[4,7],[2,6]]", [[0.6, -0.7], [-0.2, 0.4]],
     lambda: inverse([[4, 7], [2, 6]])),
    ("Inverse of 3x3 C", [[-24, 18, 5], [20, -15, -4], [-5, 4, 1]], lambda: inverse(C)),
    ("C x inverse(C) = identity", [[1, 0, 0], [0, 1, 0], [0, 0, 1]], c_times_inverse),
    ("Inverse of a singular matrix", "Error: Matrix is singular (determinant is 0)",
     lambda: inverse(SINGULAR_3X3)),
    ("Inverse of 1x1 [[2]]", [[0.5]], lambda: inverse([[2]])),
    ("Trace of A", 5, lambda: trace(A)),
    ("[[1,2],[2,1]] is symmetric", True, lambda: is_symmetric([[1, 2], [2, 1]])),
    ("A is symmetric", False, lambda: is_symmetric(A)),
    ("Rows of different length", "Error: All rows must have the same length",
     lambda: transpose([[1, 2], [3]])),
    ("Empty matrix", "Error: Matrix cannot be empty", lambda: transpose([])),
]

if __name__ == "__main__":
    sys.exit(0 if run_cases(CASES) else 1)
