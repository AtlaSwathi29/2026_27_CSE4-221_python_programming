"""Test cases for Case Study 10 (Railway Ticket Reservation System).
Run:  python test_railway_reservation.py           -> readable results
      python test_railway_reservation.py --table   -> Markdown table for the report
"""
import sys
from railway_reservation import Train


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


def new_train():
    """2 confirmed seats, 1 RAC, 1 waiting; Rs.1.5 per km."""
    return Train("Express 101", 2, 1, 1, 1.5)


def full_train():
    """Four adult passengers (30 yrs, 400 km): PNR 1001..1004."""
    train = new_train()
    for name in ("Asha", "Ravi", "Meena", "Kiran"):
        train.book(name, 30, 400)
    return train


def statuses_in_order():
    train = new_train()
    return [train.book(n, 30, 400)["status"] for n in ("A", "B", "C", "D")]


def fifth_booking():
    return full_train().book("Extra", 30, 400)


def after_cancel_confirmed():
    train = full_train()
    train.cancel(1001)
    return [train.status(p) for p in (1002, 1003, 1004)]


def after_cancel_rac():
    train = full_train()
    train.cancel(1003)
    return [train.status(p) for p in (1001, 1002, 1004)]


def after_cancel_waiting():
    train = full_train()
    train.cancel(1004)
    return [train.status(p) for p in (1001, 1002, 1003)]


def new_booking_after_cancel():
    train = full_train()
    train.cancel(1001)                  # queues move up, waiting list becomes free
    return train.book("New", 30, 400)["status"]


def double_cancel():
    train = full_train()
    train.cancel(1001)
    return train.cancel(1001)


def fare(age):
    return new_train().book("P", age, 400)["fare"]


CASES = [
    ("Fare: adult (age 30), 400 km at Rs.1.5/km", 600.0, lambda: fare(30)),
    ("Fare: senior citizen (age 65) - 40% concession", 360.0, lambda: fare(65)),
    ("Fare: exactly age 60 gets concession", 360.0, lambda: fare(60)),
    ("Fare: child age 3 travels free", 0.0, lambda: fare(3)),
    ("Fare: age 5 pays full fare", 600.0, lambda: fare(5)),
    ("Status of four bookings in order",
     ["CONFIRMED", "CONFIRMED", "RAC", "WL"], statuses_in_order),
    ("First PNR number issued", 1001, lambda: new_train().book("A", 30, 400)["pnr"]),
    ("Fifth booking when train is full", "Error: Train is full - no booking possible",
     fifth_booking),
    ("Cancel confirmed 1001: statuses of 1002, 1003, 1004",
     ["CONFIRMED", "CONFIRMED", "RAC"], after_cancel_confirmed),
    ("Cancel RAC 1003: statuses of 1001, 1002, 1004",
     ["CONFIRMED", "CONFIRMED", "RAC"], after_cancel_rac),
    ("Cancel waiting 1004: statuses of 1001, 1002, 1003",
     ["CONFIRMED", "CONFIRMED", "RAC"], after_cancel_waiting),
    ("Refund for a confirmed ticket (75% of Rs.600)", 450.0,
     lambda: full_train().cancel(1001)),
    ("Refund for an RAC ticket (75% of Rs.600)", 450.0,
     lambda: full_train().cancel(1003)),
    ("Refund for a waiting-list ticket (100% of Rs.600)", 600.0,
     lambda: full_train().cancel(1004)),
    ("New booking after a cancellation frees the waiting list", "WL",
     new_booking_after_cancel),
    ("Cancel the same ticket twice", "Error: Ticket already cancelled", double_cancel),
    ("Cancel unknown PNR", "Error: PNR not found", lambda: new_train().cancel(5555)),
    ("Age 150", "Error: Invalid age", lambda: new_train().book("A", 150, 400)),
    ("Blank passenger name", "Error: Passenger name cannot be empty",
     lambda: new_train().book(" ", 30, 400)),
    ("Distance 0 km", "Error: Distance must be positive",
     lambda: new_train().book("A", 30, 0)),
]

if __name__ == "__main__":
    sys.exit(0 if run_cases(CASES) else 1)
