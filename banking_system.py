"""
Case Study 1: Banking System
----------------------------
A beginner-friendly program that models a small bank using classes.
Features: open account, deposit, withdraw, transfer, PIN security
(account locks after 3 wrong PINs) and mini statement.

Run:  python banking_system.py          -> interactive menu
      python banking_system.py --demo   -> automatic sample run
"""
import sys

MIN_BALANCE = 500       # minimum balance that must always remain in an account
MAX_WITHDRAW = 20000    # maximum amount allowed in one withdrawal / transfer
MAX_PIN_TRIES = 3       # wrong PIN attempts allowed before the account locks


class BankError(Exception):
    """Raised whenever a banking rule is violated."""


class Account:
    """Stores the details of one customer account."""

    def __init__(self, acc_no, name, balance, pin):
        self.acc_no = acc_no
        self.name = name
        self.balance = balance
        self.pin = pin
        self.failed_tries = 0      # consecutive wrong PIN count
        self.locked = False
        self.history = []          # list of (kind, amount, balance_after)

    def check_pin(self, pin):
        """Verify the PIN; lock the account after too many wrong tries."""
        if self.locked:
            raise BankError("Account is locked")
        if pin != self.pin:
            self.failed_tries += 1
            if self.failed_tries >= MAX_PIN_TRIES:
                self.locked = True
                raise BankError("Account locked after 3 wrong PINs")
            raise BankError("Wrong PIN")
        self.failed_tries = 0      # correct PIN resets the counter

    def record(self, kind, amount):
        """Add one line to the transaction history."""
        self.history.append((kind, amount, self.balance))


class Bank:
    """Holds all accounts and performs the banking operations."""

    def __init__(self):
        self.accounts = {}         # account number -> Account
        self.next_no = 1001        # first account number

    def _get(self, acc_no):
        if acc_no not in self.accounts:
            raise BankError("Account not found")
        return self.accounts[acc_no]

    @staticmethod
    def _check_amount(amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise BankError("Amount must be a positive number")

    def open_account(self, name, deposit, pin):
        """Create an account and return its account number."""
        if not name.strip():
            raise BankError("Name cannot be empty")
        if not (len(pin) == 4 and pin.isdigit()):
            raise BankError("PIN must be exactly 4 digits")
        if deposit < MIN_BALANCE:
            raise BankError("Opening deposit must be at least " + str(MIN_BALANCE))
        acc_no = self.next_no
        self.next_no += 1
        acc = Account(acc_no, name.strip(), deposit, pin)
        acc.record("OPEN", deposit)
        self.accounts[acc_no] = acc
        return acc_no

    def deposit(self, acc_no, amount):
        acc = self._get(acc_no)
        self._check_amount(amount)
        acc.balance += amount
        acc.record("DEPOSIT", amount)
        return acc.balance

    def withdraw(self, acc_no, amount, pin):
        acc = self._get(acc_no)
        acc.check_pin(pin)
        self._check_amount(amount)
        if amount > MAX_WITHDRAW:
            raise BankError("Limit per withdrawal is " + str(MAX_WITHDRAW))
        if acc.balance - amount < MIN_BALANCE:
            raise BankError("Insufficient funds (minimum balance rule)")
        acc.balance -= amount
        acc.record("WITHDRAW", amount)
        return acc.balance

    def transfer(self, from_no, to_no, amount, pin):
        src = self._get(from_no)
        dst = self._get(to_no)
        if from_no == to_no:
            raise BankError("Cannot transfer to the same account")
        src.check_pin(pin)
        self._check_amount(amount)
        if amount > MAX_WITHDRAW:
            raise BankError("Limit per transfer is " + str(MAX_WITHDRAW))
        if src.balance - amount < MIN_BALANCE:
            raise BankError("Insufficient funds (minimum balance rule)")
        src.balance -= amount
        dst.balance += amount
        src.record("TRANSFER OUT", amount)
        dst.record("TRANSFER IN", amount)
        return src.balance

    def statement(self, acc_no):
        """Return the transaction history as a list of text lines."""
        acc = self._get(acc_no)
        lines = []
        for kind, amount, bal in acc.history:
            lines.append(f"{kind:<13} {amount:>10.2f}   balance: {bal:>10.2f}")
        return lines


def demo():
    bank = Bank()
    a = bank.open_account("Asha", 5000, "1234")
    b = bank.open_account("Ravi", 1000, "4321")
    print("Accounts opened:", a, b)
    print("Deposit 2000 to Asha -> balance", bank.deposit(a, 2000))
    print("Withdraw 1500 from Asha -> balance", bank.withdraw(a, 1500, "1234"))
    print("Transfer 3000 Asha->Ravi -> Asha balance", bank.transfer(a, b, 3000, "1234"))
    for action, call in [
        ("Withdraw 5000 from Ravi (breaks minimum balance)",
         lambda: bank.withdraw(b, 5000, "4321")),
        ("Withdraw with wrong PIN", lambda: bank.withdraw(a, 100, "0000")),
        ("Wrong PIN again", lambda: bank.withdraw(a, 100, "1111")),
        ("Wrong PIN third time", lambda: bank.withdraw(a, 100, "2222")),
        ("Correct PIN after lock", lambda: bank.withdraw(a, 100, "1234")),
    ]:
        try:
            call()
        except BankError as err:
            print(action, "->", err)
    print("\nMini statement for Ravi:")
    for line in bank.statement(b):
        print(" ", line)


def main():
    bank = Bank()
    while True:
        print("\n1.Open  2.Deposit  3.Withdraw  4.Transfer  5.Statement  6.Exit")
        choice = input("Choice: ").strip()
        try:
            if choice == "1":
                name = input("Name: ")
                dep = float(input("Opening deposit: "))
                pin = input("Set 4-digit PIN: ")
                print("Account number:", bank.open_account(name, dep, pin))
            elif choice == "2":
                acc = int(input("Account no: "))
                print("New balance:", bank.deposit(acc, float(input("Amount: "))))
            elif choice == "3":
                acc = int(input("Account no: "))
                amt = float(input("Amount: "))
                print("New balance:", bank.withdraw(acc, amt, input("PIN: ")))
            elif choice == "4":
                src = int(input("From account: "))
                dst = int(input("To account: "))
                amt = float(input("Amount: "))
                print("Your balance:", bank.transfer(src, dst, amt, input("PIN: ")))
            elif choice == "5":
                for line in bank.statement(int(input("Account no: "))):
                    print(line)
            elif choice == "6":
                print("Thank you!")
                break
            else:
                print("Invalid choice")
        except (BankError, ValueError) as err:
            print("Error:", err)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else main()
