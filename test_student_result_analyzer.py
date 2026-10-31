"""Test cases for Case Study 3 (Student Result Analyzer).
Run:  python test_student_result_analyzer.py           -> readable results
      python test_student_result_analyzer.py --table   -> Markdown table for the report
"""
import sys
from student_result_analyzer import analyse, calculate_grade, class_statistics


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


def one(marks):
    """Summary (total, percentage, grade, result) of a single student."""
    r = analyse({"S": marks})[0]
    return (r["total"], r["percentage"], r["grade"], r["result"])


def ranks():
    data = {"A": [90] * 5, "B": [90] * 5, "C": [80] * 5}
    return [(r["name"], r["rank"]) for r in analyse(data)]


def stats(key):
    data = {"A": [100, 100, 100, 100, 100],
            "B": [50, 50, 50, 50, 50],
            "C": [30, 90, 90, 90, 90]}          # C fails Maths (30)
    return class_statistics(analyse(data))[key]


CASES = [
    ("Grade at 90%", "O", lambda: calculate_grade(90)),
    ("Grade at 89.99%", "A+", lambda: calculate_grade(89.99)),
    ("Grade at 70%", "A", lambda: calculate_grade(70)),
    ("Grade at 40% (lowest pass)", "P", lambda: calculate_grade(40)),
    ("Grade at 39.99%", "F", lambda: calculate_grade(39.99)),
    ("All subjects 100", (500, 100.0, "O", "PASS"), lambda: one([100] * 5)),
    ("Marks 80,70,60,50,40 (lowest exactly 40)", (300, 60.0, "B", "PASS"),
     lambda: one([80, 70, 60, 50, 40])),
    ("One subject 39 -> fails whole result", (439, 87.8, "F", "FAIL"),
     lambda: one([100, 100, 100, 100, 39])),
    ("Only 4 marks entered", "Error: Exactly 5 marks are required",
     lambda: one([50, 50, 50, 50])),
    ("A mark of 101", "Error: Marks must be between 0 and 100",
     lambda: one([101, 50, 50, 50, 50])),
    ("A negative mark", "Error: Marks must be between 0 and 100",
     lambda: one([-1, 50, 50, 50, 50])),
    ("Ties share rank (90,90,80 totals) -> 1,1,3", [("A", 1), ("B", 1), ("C", 3)],
     ranks),
    ("Class average of totals 500, 250, 390", 380.0, lambda: stats("average")),
    ("Pass percentage (2 of 3 pass)", 66.67, lambda: stats("pass_percentage")),
    ("Topper of the class", ["A"], lambda: stats("toppers")),
    ("Highest mark in Maths (and who)", (100, ["A"]),
     lambda: stats("subject_toppers")["Maths"]),
]

if __name__ == "__main__":
    sys.exit(0 if run_cases(CASES) else 1)
