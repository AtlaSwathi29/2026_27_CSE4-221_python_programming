"""
Case Study 7: Tic-Tac-Toe with an Unbeatable Computer Player (Minimax)
----------------------------------------------------------------------
The board is a list of 9 cells (0..8): " ", "X" or "O".
The computer uses the MINIMAX algorithm: it tries every possible future game
and picks the move with the best guaranteed result. The human can never beat
it - the best a human can do is draw.

Run:  python tictactoe_ai.py          -> play against the computer
      python tictactoe_ai.py --demo   -> computer plays itself (always a draw)
"""
import sys

WIN_LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8),      # rows
             (0, 3, 6), (1, 4, 7), (2, 5, 8),      # columns
             (0, 4, 8), (2, 4, 6)]                 # diagonals


def winner(board):
    """Return 'X' or 'O' if someone has won, 'Draw' if full, else None."""
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    if " " not in board:
        return "Draw"
    return None


def empty_cells(board):
    return [i for i in range(9) if board[i] == " "]


def other(player):
    return "O" if player == "X" else "X"


def minimax(board, player, ai, depth):
    """
    Score of the board if `player` is about to move and both sides play
    perfectly. AI win = positive, AI loss = negative, draw = 0.
    Winning sooner scores higher (10 - depth).
    """
    result = winner(board)
    if result == ai:
        return 10 - depth
    if result == other(ai):
        return depth - 10
    if result == "Draw":
        return 0

    scores = []
    for cell in empty_cells(board):
        board[cell] = player                       # try the move
        scores.append(minimax(board, other(player), ai, depth + 1))
        board[cell] = " "                          # undo the move
    return max(scores) if player == ai else min(scores)


def best_move(board, ai):
    """Return the index (0-8) of the best move for the computer."""
    if len(empty_cells(board)) == 9:
        return 4                                   # centre is best; saves time
    best_cell, best_score = None, None
    for cell in empty_cells(board):
        board[cell] = ai
        score = minimax(board, other(ai), ai, 1)
        board[cell] = " "
        if best_score is None or score > best_score:
            best_cell, best_score = cell, score
    return best_cell


def show(board):
    for r in range(3):
        row = board[3 * r: 3 * r + 3]
        print(" " + " | ".join(c if c != " " else str(3 * r + i + 1)
                               for i, c in enumerate(row)))
        if r < 2:
            print("---+---+---")


def demo():
    board = [" "] * 9
    turn = "X"
    while winner(board) is None:
        board[best_move(board, turn)] = turn
        turn = other(turn)
    show(board)
    print("Result:", winner(board))


def main():
    human = input("Choose X (moves first) or O: ").strip().upper()
    if human not in ("X", "O"):
        human = "X"
    ai = other(human)
    board = [" "] * 9
    turn = "X"
    while winner(board) is None:
        show(board)
        if turn == human:
            try:
                cell = int(input("Your move (1-9): ")) - 1
            except ValueError:
                print("Enter a number 1-9")
                continue
            if cell not in empty_cells(board):
                print("Invalid or occupied cell")
                continue
            board[cell] = human
        else:
            board[best_move(board, ai)] = ai
        turn = other(turn)
    show(board)
    result = winner(board)
    print("It's a draw!" if result == "Draw" else result + " wins!")


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else main()
