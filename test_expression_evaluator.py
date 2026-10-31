"""Test cases for Case Study 9 (Infix Expression Evaluator).
Run:  python test_expression_evaluator.py           -> readable results
      python test_expression_evaluator.py --table   -> Markdown table for the report
"""
import sys
from expression_evaluator import evaluate, to_postfix, tokenize


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


def postfix_text(expression):
    """Postfix form as readable text, e.g. '2 3 4 * +'."""
    parts = []
    for tok in to_postfix(tokenize(expression)):
        parts.append(str(int(tok)) if isinstance(tok, float) else tok)
    return " ".join(parts)


CASES = [
    ("2 + 3 * 4  (multiplication first)", 14, lambda: evaluate("2 + 3 * 4")),
    ("(2 + 3) * 4  (brackets first)", 20, lambda: evaluate("(2 + 3) * 4")),
    ("10 / 4  (decimal result)", 2.5, lambda: evaluate("10 / 4")),
    ("100 - 10 - 5  (left to right)", 85, lambda: evaluate("100 - 10 - 5")),
    ("100 / 10 / 5  (left to right)", 2, lambda: evaluate("100 / 10 / 5")),
    ("2 ^ 3 ^ 2  (power is right-to-left)", 512, lambda: evaluate("2 ^ 3 ^ 2")),
    ("-2 ^ 2  (unary minus after power)", -4, lambda: evaluate("-2 ^ 2")),
    ("2 * -3  (unary minus after operator)", -6, lambda: evaluate("2 * -3")),
    ("5 - -3", 8, lambda: evaluate("5 - -3")),
    ("-(2 + 3)", -5, lambda: evaluate("-(2 + 3)")),
    ("+5 + 3  (unary plus)", 8, lambda: evaluate("+5 + 3")),
    ("1.5 + 2.5  (decimals)", 4, lambda: evaluate("1.5 + 2.5")),
    ("2 ^ -2", 0.25, lambda: evaluate("2 ^ -2")),
    ("((1+2)*(3+4))/7  (nested brackets, no spaces)", 3,
     lambda: evaluate("((1+2)*(3+4))/7")),
    ("3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3  (classic example)", 3.000122,
     lambda: evaluate("3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3")),
    ("Postfix of 2 + 3 * 4", "2 3 4 * +", lambda: postfix_text("2 + 3 * 4")),
    ("Postfix of (2 + 3) * 4", "2 3 + 4 *", lambda: postfix_text("(2 + 3) * 4")),
    ("Missing closing bracket: (2 + 3", "Error: Mismatched parentheses",
     lambda: evaluate("(2 + 3")),
    ("Extra closing bracket: 2 + 3)", "Error: Mismatched parentheses",
     lambda: evaluate("2 + 3)")),
    ("Division by zero: 5 / 0", "Error: Division by zero", lambda: evaluate("5 / 0")),
    ("Operator without operand: 2 +", "Error: Invalid expression",
     lambda: evaluate("2 +")),
    ("Two numbers, no operator: 2 3", "Error: Invalid expression",
     lambda: evaluate("2 3")),
    ("Empty brackets: ()", "Error: Invalid expression", lambda: evaluate("()")),
    ("Invalid character: 7 & 2", "Error: Invalid character: &",
     lambda: evaluate("7 & 2")),
    ("Bad number: 1.2.3 + 1", "Error: Invalid number: 1.2.3",
     lambda: evaluate("1.2.3 + 1")),
    ("Square root of negative: (-8) ^ 0.5", "Error: Result is not a real number",
     lambda: evaluate("(-8) ^ 0.5")),
    ("Empty expression", "Error: Expression is empty", lambda: evaluate("   ")),
]

if __name__ == "__main__":
    sys.exit(0 if run_cases(CASES) else 1)
