"""
Case Study 4: Inventory and Billing System
------------------------------------------
A shop keeps products with price, stock and GST rate. A bill is generated for
a basket of items: stock is checked and reduced, a volume discount is applied
(5% if subtotal >= 2000, 10% if >= 5000), GST is calculated on the discounted
amount, and low-stock items are reported.

Run:  python inventory_billing.py          -> interactive menu
      python inventory_billing.py --demo   -> automatic sample run
"""
import sys

LOW_STOCK_LIMIT = 5


class StoreError(Exception):
    """Raised for invalid products, quantities or insufficient stock."""


class Store:
    def __init__(self):
        # code -> {"name", "price", "stock", "gst"}
        self.products = {}

    def add_product(self, code, name, price, stock, gst_percent):
        if price <= 0 or stock < 0 or not (0 <= gst_percent <= 28):
            raise StoreError("Invalid price, stock or GST rate")
        self.products[code] = {"name": name, "price": price,
                               "stock": stock, "gst": gst_percent}

    def restock(self, code, quantity):
        if code not in self.products:
            raise StoreError("Product not found")
        if quantity <= 0:
            raise StoreError("Quantity must be positive")
        self.products[code]["stock"] += quantity

    @staticmethod
    def discount_rate(subtotal):
        """Volume discount slab."""
        if subtotal >= 5000:
            return 0.10
        if subtotal >= 2000:
            return 0.05
        return 0.0

    def make_bill(self, items):
        """
        items: list of (code, quantity).
        All items are checked first so that stock changes only if the whole
        bill is valid.
        """
        if not items:
            raise StoreError("Cart is empty")
        lines = []
        subtotal = 0.0
        for code, qty in items:
            if code not in self.products:
                raise StoreError("Product not found: " + str(code))
            if qty <= 0:
                raise StoreError("Quantity must be positive")
            product = self.products[code]
            if qty > product["stock"]:
                raise StoreError("Insufficient stock for " + product["name"])
            amount = product["price"] * qty
            lines.append((code, product["name"], qty, product["price"],
                          amount, product["gst"]))
            subtotal += amount

        rate = self.discount_rate(subtotal)
        discount = subtotal * rate
        gst_total = 0.0
        for line in lines:
            discounted_amount = line[4] * (1 - rate)
            gst_total += discounted_amount * line[5] / 100

        # everything is valid, so reduce the stock now
        for code, qty in items:
            self.products[code]["stock"] -= qty

        return {"lines": lines,
                "subtotal": round(subtotal, 2),
                "discount": round(discount, 2),
                "gst": round(gst_total, 2),
                "total": round(subtotal - discount + gst_total, 2)}

    def low_stock(self):
        """Names of products whose stock is below the limit."""
        return sorted(p["name"] for p in self.products.values()
                      if p["stock"] < LOW_STOCK_LIMIT)


def format_bill(bill):
    out = [f"{'Item':<14}{'Qty':>4}{'Price':>9}{'Amount':>11}"]
    for _, name, qty, price, amount, _ in bill["lines"]:
        out.append(f"{name:<14}{qty:>4}{price:>9.2f}{amount:>11.2f}")
    out.append("-" * 38)
    out.append(f"{'Subtotal':<27}{bill['subtotal']:>11.2f}")
    out.append(f"{'Discount':<27}{0 - bill['discount']:>11.2f}")
    out.append(f"{'GST':<27}{bill['gst']:>11.2f}")
    out.append(f"{'TOTAL':<27}{bill['total']:>11.2f}")
    return "\n".join(out)


def demo():
    store = Store()
    store.add_product("P1", "Notebook", 60, 100, 12)
    store.add_product("P2", "Pen Pack", 120, 40, 12)
    store.add_product("P3", "Calculator", 850, 10, 18)
    store.add_product("P4", "Backpack", 1500, 6, 18)

    print("BILL 1")
    print(format_bill(store.make_bill([("P1", 10), ("P2", 2)])))
    print("\nBILL 2 (qualifies for 10% discount)")
    print(format_bill(store.make_bill([("P3", 3), ("P4", 4)])))
    print("\nLow stock items:", store.low_stock())
    try:
        store.make_bill([("P4", 5)])
    except StoreError as err:
        print("Bill 3 error:", err)


def main():
    store = Store()
    while True:
        print("\n1.Add product 2.Restock 3.Bill 4.Low stock 5.Exit")
        choice = input("Choice: ").strip()
        try:
            if choice == "1":
                store.add_product(input("Code: "), input("Name: "),
                                  float(input("Price: ")), int(input("Stock: ")),
                                  float(input("GST %: ")))
            elif choice == "2":
                store.restock(input("Code: "), int(input("Quantity: ")))
            elif choice == "3":
                items = []
                while True:
                    code = input("Product code (blank to finish): ").strip()
                    if not code:
                        break
                    items.append((code, int(input("Quantity: "))))
                print(format_bill(store.make_bill(items)))
            elif choice == "4":
                print("Low stock:", store.low_stock())
            elif choice == "5":
                break
            else:
                print("Invalid choice")
        except (StoreError, ValueError) as err:
            print("Error:", err)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else main()
