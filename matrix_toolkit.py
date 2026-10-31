"""
Case Study 8: Matrix Operations Toolkit
---------------------------------------
Matrices are lists of rows. Supports addition, subtraction, multiplication,
transpose, trace, symmetry check, determinant (recursive cofactor expansion)
and inverse (adjugate method) with proper error checking.

Run:  python matrix_toolkit.py          -> interactive menu
      python matrix_toolkit.py --demo   -> automatic sample run
"""
import sys


def validate(m):
    """Matrix must be non-empty with all rows of equal length."""
    if not m or not m[0]:
        raise ValueError("Matrix cannot be empty")
    width = len(m[0])
    for row in m:
        if len(row) != width:
            raise ValueError("All rows must have the same length")


def shape(m):
    validate(m)
    return len(m), len(m[0])


def add(a, b):
    if shape(a) != shape(b):
        raise ValueError("Matrices must have the same size to add")
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def subtract(a, b):
    if shape(a) != shape(b):
        raise ValueError("Matrices must have the same size to subtract")
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def multiply(a, b):
    """Rows of A times columns of B. Needs columns(A) == rows(B)."""
    if shape(a)[1] != shape(b)[0]:
        raise ValueError("Columns of A must equal rows of B")
    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(b[0])):
            total = 0
            for k in range(len(b)):
                total += a[i][k] * b[k][j]
            row.append(total)
        result.append(row)
    return result


def transpose(m):
    validate(m)
    return [[m[i][j] for i in range(len(m))] for j in range(len(m[0]))]


def require_square(m):
    rows, cols = shape(m)
    if rows != cols:
        raise ValueError("Matrix must be square")
    return rows


def trace(m):
    n = require_square(m)
    return sum(m[i][i] for i in range(n))


def is_symmetric(m):
    require_square(m)
    return m == transpose(m)


def minor(m, row, col):
    """Matrix with the given row and column removed."""
    return [[m[i][j] for j in range(len(m)) if j != col]
            for i in range(len(m)) if i != row]


def determinant(m):
    """Cofactor expansion along the first row (recursive)."""
    n = require_square(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    total = 0
    for col in range(n):
        sign = 1 if col % 2 == 0 else -1
        total += sign * m[0][col] * determinant(minor(m, 0, col))
    return total


def inverse(m):
    """Inverse = adjugate / determinant. Singular matrices have no inverse."""
    n = require_square(m)
    det = determinant(m)
    if abs(det) < 1e-12:
        raise ValueError("Matrix is singular (determinant is 0)")
    if n == 1:
        return [[round(1 / m[0][0], 4)]]
    cofactors = [[((-1) ** (i + j)) * determinant(minor(m, i, j))
                  for j in range(n)] for i in range(n)]
    adjugate = transpose(cofactors)
    return [[round(value / det, 4) for value in row] for row in adjugate]


def show(title, m):
    print(title)
    for row in m:
        print("  ", row)


def demo():
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    show("A =", a)
    show("B =", b)
    show("A + B =", add(a, b))
    show("A - B =", subtract(a, b))
    show("A x B =", multiply(a, b))
    show("Transpose of A =", transpose(a))
    print("Trace of A =", trace(a), "| Symmetric?", is_symmetric(a))

    c = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
    show("\nC =", c)
    print("Determinant of C =", determinant(c))
    show("Inverse of C =", inverse(c))
    show("C x inverse(C) =", [[round(v, 4) for v in row]
                              for row in multiply(c, inverse(c))])
    try:
        inverse([[1, 2], [2, 4]])
    except ValueError as err:
        print("\nInverse of [[1,2],[2,4]] ->", err)


def read_matrix(name):
    rows = int(input(f"Rows of {name}: "))
    return [[float(x) for x in input(f"  Row {i + 1} (space separated): ").split()]
            for i in range(rows)]


def main():
    while True:
        print("\n1.Add 2.Subtract 3.Multiply 4.Transpose 5.Determinant "
              "6.Inverse 7.Exit")
        choice = input("Choice: ").strip()
        try:
            if choice in ("1", "2", "3"):
                a, b = read_matrix("A"), read_matrix("B")
                op = {"1": add, "2": subtract, "3": multiply}[choice]
                show("Result:", op(a, b))
            elif choice == "4":
                show("Result:", transpose(read_matrix("A")))
            elif choice == "5":
                print("Determinant:", determinant(read_matrix("A")))
            elif choice == "6":
                show("Inverse:", inverse(read_matrix("A")))
            elif choice == "7":
                break
            else:
                print("Invalid choice")
        except ValueError as err:
            print("Error:", err)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else main()
