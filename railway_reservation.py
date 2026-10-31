"""
Case Study 10: Railway Ticket Reservation System
------------------------------------------------
A train has limited CONFIRMED seats, then RAC (Reservation Against
Cancellation) places, then a WAITING list. When a ticket is cancelled, the
queues move up automatically: RAC -> Confirmed, Waiting -> RAC.
Fare = distance x rate; children under 5 travel free, senior citizens (60+)
get 40% concession. Refund: 75% for Confirmed/RAC, 100% for Waiting list.

Run:  python railway_reservation.py          -> interactive menu
      python railway_reservation.py --demo   -> automatic sample run
"""
import sys


class RailwayError(Exception):
    """Raised for invalid bookings or cancellations."""


class Train:
    def __init__(self, name, confirmed_seats, rac_seats, waiting_seats, rate_per_km):
        self.name = name
        self.capacity = {"CONFIRMED": confirmed_seats, "RAC": rac_seats,
                         "WL": waiting_seats}
        self.rate = rate_per_km
        # each queue holds PNR numbers in booking order
        self.queues = {"CONFIRMED": [], "RAC": [], "WL": []}
        self.tickets = {}          # pnr -> ticket dictionary
        self.next_pnr = 1001

    @staticmethod
    def fare_for(age, distance_km, rate):
        base = distance_km * rate
        if age < 5:
            return 0.0
        if age >= 60:
            return round(base * 0.60, 2)
        return round(base, 2)

    def book(self, name, age, distance_km):
        """Book a ticket and return the ticket dictionary."""
        if not name.strip():
            raise RailwayError("Passenger name cannot be empty")
        if age < 0 or age > 120:
            raise RailwayError("Invalid age")
        if distance_km <= 0:
            raise RailwayError("Distance must be positive")

        status = None
        for queue in ("CONFIRMED", "RAC", "WL"):          # first free queue
            if len(self.queues[queue]) < self.capacity[queue]:
                status = queue
                break
        if status is None:
            raise RailwayError("Train is full - no booking possible")

        pnr = self.next_pnr
        self.next_pnr += 1
        ticket = {"pnr": pnr, "name": name.strip(), "age": age,
                  "fare": self.fare_for(age, distance_km, self.rate),
                  "status": status}
        self.tickets[pnr] = ticket
        self.queues[status].append(pnr)
        return ticket

    def cancel(self, pnr):
        """Cancel a ticket, promote waiting passengers and return the refund."""
        if pnr not in self.tickets:
            raise RailwayError("PNR not found")
        ticket = self.tickets[pnr]
        if ticket["status"] == "CANCELLED":
            raise RailwayError("Ticket already cancelled")

        old_status = ticket["status"]
        self.queues[old_status].remove(pnr)
        ticket["status"] = "CANCELLED"
        refund_rate = 1.0 if old_status == "WL" else 0.75
        refund = round(ticket["fare"] * refund_rate, 2)

        # move the queues up
        if old_status == "CONFIRMED" and self.queues["RAC"]:
            self._promote("RAC", "CONFIRMED")
        if old_status in ("CONFIRMED", "RAC") and self.queues["WL"]:
            self._promote("WL", "RAC")
        return refund

    def _promote(self, from_queue, to_queue):
        """Move the first passenger of one queue to the next better queue."""
        pnr = self.queues[from_queue].pop(0)
        self.queues[to_queue].append(pnr)
        self.tickets[pnr]["status"] = to_queue

    def status(self, pnr):
        if pnr not in self.tickets:
            raise RailwayError("PNR not found")
        return self.tickets[pnr]["status"]


def demo():
    train = Train("Express 101", confirmed_seats=2, rac_seats=1,
                  waiting_seats=1, rate_per_km=1.5)
    print("Booking tickets (2 confirmed, 1 RAC, 1 waiting)")
    for name, age in [("Asha", 30), ("Ravi", 65), ("Meena", 3), ("Kiran", 40)]:
        t = train.book(name, age, 400)
        print(f"  PNR {t['pnr']}  {t['name']:<6} age {t['age']:<3} "
              f"fare Rs.{t['fare']:<8} {t['status']}")
    try:
        train.book("Extra", 25, 400)
    except RailwayError as err:
        print("  Extra passenger ->", err)

    print("\nCancelling PNR 1001 (Asha, confirmed)")
    print("  Refund: Rs.", train.cancel(1001))
    for pnr in (1002, 1003, 1004):
        print(f"  PNR {pnr} is now {train.status(pnr)}")


def main():
    train = Train("Express 101", 3, 2, 2, 1.5)
    while True:
        print("\n1.Book  2.Cancel  3.Check status  4.Exit")
        choice = input("Choice: ").strip()
        try:
            if choice == "1":
                t = train.book(input("Name: "), int(input("Age: ")),
                               float(input("Distance (km): ")))
                print("Booked! PNR", t["pnr"], "| Fare Rs.", t["fare"],
                      "|", t["status"])
            elif choice == "2":
                print("Refund: Rs.", train.cancel(int(input("PNR: "))))
            elif choice == "3":
                print("Status:", train.status(int(input("PNR: "))))
            elif choice == "4":
                break
            else:
                print("Invalid choice")
        except (RailwayError, ValueError) as err:
            print("Error:", err)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else main()
