"""Test cases for Case Study 1 (Banking System).
Run:  python test_banking_system.py           -> readable results
      python test_banking_system.py --table   -> Markdown table for the report
"""
import sys
from banking_system import Bank


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
    """Bank with Asha (1001, Rs.5000, PIN 1234) and Ravi (1002, Rs.1000, PIN 4321)."""
    bank = Bank()
    bank.open_account("Asha", 5000, "1234")
    bank.open_account("Ravi", 1000, "4321")
    return bank


def three_wrong_pins():
    bank = fresh()
    for pin in ("0000", "1111"):
        try:
            bank.withdraw(1001, 100, pin)
        except Exception:
            pass
    return bank.withdraw(1001, 100, "2222")


def correct_pin_after_lock():
    bank = fresh()
    for pin in ("0000", "1111", "2222"):
        try:
            bank.withdraw(1001, 100, pin)
        except Exception:
            pass
    return bank.withdraw(1001, 100, "1234")


def transfer_balances():
    bank = fresh()
    bank.transfer(1001, 1002, 1000, "1234")
    return (bank.accounts[1001].balance, bank.accounts[1002].balance)


def over_limit():
    bank = fresh()
    bank.deposit(1001, 30000)
    return bank.withdraw(1001, 25000, "1234")


def statement_length():
    bank = fresh()
    bank.deposit(1001, 100)
    bank.withdraw(1001, 50, "1234")
    return len(bank.statement(1001))


CASES = [
    ("Open account: Asha, Rs.5000, PIN 1234", 1001,
     lambda: Bank().open_account("Asha", 5000, "1234")),
    ("Open account with deposit Rs.400 (below minimum)",
     "Error: Opening deposit must be at least 500",
     lambda: Bank().open_account("Asha", 400, "1234")),
    ("Open account with PIN '12a4'", "Error: PIN must be exactly 4 digits",
     lambda: Bank().open_account("Asha", 5000, "12a4")),
    ("Open account with blank name", "Error: Name cannot be empty",
     lambda: Bank().open_account("  ", 5000, "1234")),
    ("Deposit Rs.2000 into balance 5000", 7000, lambda: fresh().deposit(1001, 2000)),
    ("Deposit Rs.-50", "Error: Amount must be a positive number",
     lambda: fresh().deposit(1001, -50)),
    ("Withdraw Rs.1500 with correct PIN", 3500,
     lambda: fresh().withdraw(1001, 1500, "1234")),
    ("Withdraw Rs.4600 (balance would fall to 400)",
     "Error: Insufficient funds (minimum balance rule)",
     lambda: fresh().withdraw(1001, 4600, "1234")),
    ("Withdraw Rs.25000 (above per-withdrawal limit)",
     "Error: Limit per withdrawal is 20000", over_limit),
    ("Withdraw with wrong PIN", "Error: Wrong PIN",
     lambda: fresh().withdraw(1001, 100, "0000")),
    ("Third wrong PIN in a row", "Error: Account locked after 3 wrong PINs",
     three_wrong_pins),
    ("Correct PIN after account is locked", "Error: Account is locked",
     correct_pin_after_lock),
    ("Transfer Rs.1000 Asha -> Ravi (balances after)", (4000, 2000),
     transfer_balances),
    ("Transfer to the same account", "Error: Cannot transfer to the same account",
     lambda: fresh().transfer(1001, 1001, 100, "1234")),
    ("Transfer to a non-existent account", "Error: Account not found",
     lambda: fresh().transfer(1001, 9999, 100, "1234")),
    ("Statement lines after open + deposit + withdraw", 3, statement_length),
]

if __name__ == "__main__":
    sys.exit(0 if run_cases(CASES) else 1)
