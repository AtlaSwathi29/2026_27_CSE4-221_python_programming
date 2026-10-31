"""Test cases for Case Study 2 (Library Management System).
Run:  python test_library_management.py           -> readable results
      python test_library_management.py --table   -> Markdown table for the report
"""
import sys
from datetime import date
from library_management import Library

ISSUE = date(2026, 10, 1)      # due date is 15 Oct 2026 (14-day loan)


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


def fresh():
    """B1 (2 copies), B2, B3, B4 (1 copy each); members M1 and M2."""
    lib = Library()
    lib.add_book("B1", "Python Crash Course", "Eric Matthes", 2)
    lib.add_book("B2", "Learning Python", "Mark Lutz", 1)
    lib.add_book("B3", "Automate the Boring Stuff", "Al Sweigart", 1)
    lib.add_book("B4", "Fluent Python", "Luciano Ramalho", 1)
    lib.register_member("M1", "Meena")
    lib.register_member("M2", "Karthik")
    return lib


def issue_three_then_fourth():
    lib = fresh()
    for book in ("B1", "B2", "B3"):
        lib.issue_book("M1", book, ISSUE)
    return lib.issue_book("M1", "B4", ISSUE)


def no_copy_left():
    lib = fresh()
    lib.issue_book("M1", "B2", ISSUE)
    return lib.issue_book("M2", "B2", ISSUE)


def duplicate_issue():
    lib = fresh()
    lib.issue_book("M1", "B1", ISSUE)
    return lib.issue_book("M1", "B1", ISSUE)


def return_fine(return_day):
    lib = fresh()
    lib.issue_book("M1", "B1", ISSUE)
    return lib.return_book("M1", "B1", return_day)


def available_after_return():
    lib = fresh()
    lib.issue_book("M1", "B2", ISSUE)
    lib.return_book("M1", "B2", date(2026, 10, 5))
    return lib.books["B2"]["available"]


def overdue():
    lib = fresh()
    lib.issue_book("M1", "B1", ISSUE)
    return lib.overdue_report(date(2026, 10, 25))


def extra_copies():
    lib = fresh()
    lib.add_book("B1", "Python Crash Course", "Eric Matthes", 3)
    return (lib.books["B1"]["copies"], lib.books["B1"]["available"])


CASES = [
    ("Issue B1 to M1 on 2026-10-01 (due date)", "2026-10-15",
     lambda: str(fresh().issue_book("M1", "B1", ISSUE))),
    ("Issue a 4th book to M1 (limit is 3)", "Error: Borrowing limit reached",
     issue_three_then_fourth),
    ("M2 borrows B2 after M1 took the only copy", "Error: No copy available",
     no_copy_left),
    ("M1 borrows the same book twice", "Error: Member already has this book",
     duplicate_issue),
    ("Issue to unknown member", "Error: Member not found",
     lambda: fresh().issue_book("M9", "B1", ISSUE)),
    ("Issue unknown book", "Error: Book not found",
     lambda: fresh().issue_book("M1", "B9", ISSUE)),
    ("Return on due date (15 Oct) - fine", 0, lambda: return_fine(date(2026, 10, 15))),
    ("Return 5 days late (20 Oct) - fine", 10, lambda: return_fine(date(2026, 10, 20))),
    ("Return before issue date", "Error: Return date is before issue date",
     lambda: return_fine(date(2026, 9, 30))),
    ("Return a book never issued", "Error: This book was not issued to the member",
     lambda: fresh().return_book("M1", "B1", ISSUE)),
    ("Available copies of B2 after issue + return", 1, available_after_return),
    ("Search 'PYTHON' (case-insensitive)", ["B1", "B2", "B4"],
     lambda: fresh().search("PYTHON")),
    ("Search author 'lutz'", ["B2"], lambda: fresh().search("lutz")),
    ("Search 'xyz' (no match)", [], lambda: fresh().search("xyz")),
    ("Overdue report on 25 Oct for B1 issued 1 Oct",
     [("Meena", "Python Crash Course", 10, 20)], overdue),
    ("Add 3 more copies of existing B1 (copies, available)", (5, 5), extra_copies),
    ("Register the same member id twice", "Error: Member already registered",
     lambda: fresh().register_member("M1", "Someone")),
]

if __name__ == "__main__":
    sys.exit(0 if run_cases(CASES) else 1)
