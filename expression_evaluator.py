"""
Case Study 9: Infix Expression Evaluator using Stacks
-----------------------------------------------------
Evaluates arithmetic expressions such as  3 + 4 * (2 - 1) ^ 2  without using
eval(). Steps:
  1. Tokenize   : split text into numbers, operators and brackets
  2. To postfix : Shunting-yard algorithm (uses a stack for operators)
  3. Evaluate   : postfix evaluation (uses a stack for numbers)
Supports + - * / ^ (power), brackets, decimals and unary minus (-5, 2*-3).

Run:  python expression_evaluator.py          -> type expressions
      python expression_evaluator.py --demo   -> automatic sample run
"""
import sys

PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "neg": 3, "^": 4}
RIGHT_ASSOCIATIVE = {"^"}          # 2^3^2 means 2^(3^2)


def tokenize(expression):
    """Convert the text into a list of numbers (float) and operator strings."""
    tokens = []
    i = 0
    while i < len(expression):
        ch = expression[i]
        if ch == " ":
            i += 1
        elif ch.isdigit() or ch == ".":
            start = i
            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            try:
                tokens.append(float(expression[start:i]))
            except ValueError:
                raise ValueError("Invalid number: " + expression[start:i])
        elif ch in "+-*/^()":
            # + or - is UNARY if it appears at the start, after '(' or after an operator
            previous = tokens[-1] if tokens else None
            is_unary = previous is None or previous == "(" or \
                (isinstance(previous, str) and previous not in (")",))
            if ch == "-" and is_unary:
                tokens.append("neg")
            elif ch == "+" and is_unary:
                pass                               # unary plus changes nothing
            else:
                tokens.append(ch)
            i += 1
        else:
            raise ValueError("Invalid character: " + ch)
    return tokens


def to_postfix(tokens):
    """Shunting-yard algorithm: infix tokens -> postfix (reverse Polish)."""
    output, stack = [], []
    for tok in tokens:
        if isinstance(tok, float):
            output.append(tok)
        elif tok == "(":
            stack.append(tok)
        elif tok == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses")
            stack.pop()                            # discard the '('
        elif tok == "neg":
            stack.append(tok)                      # prefix operator: just push
        else:                                      # binary operator
            while stack and stack[-1] != "(" and (
                    PRECEDENCE[stack[-1]] > PRECEDENCE[tok] or
                    (PRECEDENCE[stack[-1]] == PRECEDENCE[tok]
                     and tok not in RIGHT_ASSOCIATIVE)):
                output.append(stack.pop())
            stack.append(tok)
    while stack:
        if stack[-1] == "(":
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())
    return output


def evaluate_postfix(postfix):
    """Evaluate a postfix list using a stack of numbers."""
    stack = []
    for tok in postfix:
        if isinstance(tok, float):
            stack.append(tok)
        elif tok == "neg":
            if not stack:
                raise ValueError("Invalid expression")
            stack.append(-stack.pop())
        else:
            if len(stack) < 2:
                raise ValueError("Invalid expression")
            right = stack.pop()
            left = stack.pop()
            if tok == "+":
                stack.append(left + right)
            elif tok == "-":
                stack.append(left - right)
            elif tok == "*":
                stack.append(left * right)
            elif tok == "/":
                if right == 0:
                    raise ValueError("Division by zero")
                stack.append(left / right)
            elif tok == "^":
                value = left ** right
                if isinstance(value, complex):
                    raise ValueError("Result is not a real number")
                stack.append(value)
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack[0]


def evaluate(expression):
    """Full pipeline. Returns an int when the answer is a whole number."""
    if not expression.strip():
        raise ValueError("Expression is empty")
    result = evaluate_postfix(to_postfix(tokenize(expression)))
    return int(result) if result == int(result) else round(result, 6)


def demo():
    samples = ["2 + 3 * 4", "(2 + 3) * 4", "10 / 4", "2 ^ 3 ^ 2", "-2 ^ 2",
               "2 * -3", "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3",
               "(2 + 3", "5 / 0", "2 +", "7 & 2"]
    for text in samples:
        try:
            print(f"{text:<32} = {evaluate(text)}")
        except ValueError as err:
            print(f"{text:<32} -> Error: {err}")


def main():
    print("Type an expression (blank line to quit)")
    while True:
        text = input("> ")
        if not text.strip():
            break
        try:
            print("=", evaluate(text))
        except ValueError as err:
            print("Error:", err)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else main()
