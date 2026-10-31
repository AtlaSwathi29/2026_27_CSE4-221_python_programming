"""
Case Study 2: Library Management System
---------------------------------------
Manages books and members. Members can borrow up to 3 books for 14 days;
late returns are charged a fine of Rs. 2 per day. Includes search and an
overdue report.

Run:  python library_management.py          -> interactive menu
      python library_management.py --demo   -> automatic sample run
"""
import sys
from datetime import date, timedelta

LOAN_DAYS = 14       # number of days a book can be kept
FINE_PER_DAY = 2     # fine in rupees for every late day
MAX_BOOKS = 3        # maximum books one member can hold


class LibraryError(Exception):
    """Raised when a library rule is violated."""


class Library:
    def __init__(self):
        # book_id -> {"title", "author", "copies", "available"}
        self.books = {}
        # member_id -> {"name", "issued": {book_id: issue_date}}
        self.members = {}

    def add_book(self, book_id, title, author, copies=1):
        if copies <= 0:
            raise LibraryError("Copies must be positive")
        if book_id in self.books:                 # same book: add more copies
            self.books[book_id]["copies"] += copies
            self.books[book_id]["available"] += copies
        else:
            self.books[book_id] = {"title": title, "author": author,
                                   "copies": copies, "available": copies}

    def register_member(self, member_id, name):
        if member_id in self.members:
            raise LibraryError("Member already registered")
        if not name.strip():
            raise LibraryError("Name cannot be empty")
        self.members[member_id] = {"name": name.strip(), "issued": {}}

    def issue_book(self, member_id, book_id, issue_date):
        """Issue a book and return its due date."""
        if member_id not in self.members:
            raise LibraryError("Member not found")
        if book_id not in self.books:
            raise LibraryError("Book not found")
        member = self.members[member_id]
        book = self.books[book_id]
        if book_id in member["issued"]:
            raise LibraryError("Member already has this book")
        if len(member["issued"]) >= MAX_BOOKS:
            raise LibraryError("Borrowing limit reached")
        if book["available"] == 0:
            raise LibraryError("No copy available")
        member["issued"][book_id] = issue_date
        book["available"] -= 1
        return issue_date + timedelta(days=LOAN_DAYS)

    def return_book(self, member_id, book_id, return_date):
        """Return a book and give back the fine (0 if on time)."""
        if member_id not in self.members:
            raise LibraryError("Member not found")
        member = self.members[member_id]
        if book_id not in member["issued"]:
            raise LibraryError("This book was not issued to the member")
        issue_date = member["issued"][book_id]
        if return_date < issue_date:
            raise LibraryError("Return date is before issue date")
        due_date = issue_date + timedelta(days=LOAN_DAYS)
        days_late = max(0, (return_date - due_date).days)
        del member["issued"][book_id]
        self.books[book_id]["available"] += 1
        return days_late * FINE_PER_DAY

    def search(self, keyword):
        """Return ids of books whose title or author contains the keyword."""
        key = keyword.strip().lower()
        found = []
        for book_id, book in self.books.items():
            if key in book["title"].lower() or key in book["author"].lower():
                found.append(book_id)
        return sorted(found)

    def overdue_report(self, today):
        """List (member name, book title, days late, fine) for late books."""
        report = []
        for member in self.members.values():
            for book_id, issue_date in member["issued"].items():
                days_late = (today - (issue_date + timedelta(days=LOAN_DAYS))).days
                if days_late > 0:
                    report.append((member["name"], self.books[book_id]["title"],
                                   days_late, days_late * FINE_PER_DAY))
        return report


def demo():
    lib = Library()
    lib.add_book("B1", "Python Crash Course", "Eric Matthes", 2)
    lib.add_book("B2", "Learning Python", "Mark Lutz", 1)
    lib.add_book("B3", "Automate the Boring Stuff", "Al Sweigart", 1)
    lib.add_book("B4", "Fluent Python", "Luciano Ramalho", 1)
    lib.register_member("M1", "Meena")
    lib.register_member("M2", "Karthik")

    start = date(2026, 10, 1)
    print("Search 'python':", lib.search("python"))
    print("Due date for B1 (M1):", lib.issue_book("M1", "B1", start))
    lib.issue_book("M1", "B2", start)
    lib.issue_book("M1", "B3", start)
    for action, call in [
        ("M1 borrows 4th book", lambda: lib.issue_book("M1", "B4", start)),
        ("M2 borrows B2 (no copy left)", lambda: lib.issue_book("M2", "B2", start)),
    ]:
        try:
            call()
        except LibraryError as err:
            print(action, "->", err)
    print("Overdue report on 25 Oct:", lib.overdue_report(date(2026, 10, 25)))
    print("Fine returning B1 on 10 Oct :", lib.return_book("M1", "B1", date(2026, 10, 10)))
    print("Fine returning B2 on 20 Oct :", lib.return_book("M1", "B2", date(2026, 10, 20)))


def main():
    lib = Library()
    while True:
        print("\n1.Add book 2.Register member 3.Issue 4.Return 5.Search 6.Exit")
        choice = input("Choice: ").strip()
        try:
            if choice == "1":
                lib.add_book(input("Book id: "), input("Title: "), input("Author: "),
                             int(input("Copies: ")))
            elif choice == "2":
                lib.register_member(input("Member id: "), input("Name: "))
            elif choice == "3":
                due = lib.issue_book(input("Member id: "), input("Book id: "), date.today())
                print("Issued. Due date:", due)
            elif choice == "4":
                fine = lib.return_book(input("Member id: "), input("Book id: "), date.today())
                print("Returned. Fine: Rs.", fine)
            elif choice == "5":
                print("Matches:", lib.search(input("Keyword: ")))
            elif choice == "6":
                break
            else:
                print("Invalid choice")
        except (LibraryError, ValueError) as err:
            print("Error:", err)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else main()
