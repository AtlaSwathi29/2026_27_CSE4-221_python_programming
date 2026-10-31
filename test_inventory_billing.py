"""Test cases for Case Study 4 (Inventory and Billing System).
Run:  python test_inventory_billing.py           -> readable results
      python test_inventory_billing.py --table   -> Markdown table for the report
"""
import sys
from inventory_billing import Store


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
    """P1 Notebook Rs.60 x100 (GST 12%), P2 Calculator Rs.850 x10 (18%),
    P3 Backpack Rs.1500 x6 (18%)."""
    store = Store()
    store.add_product("P1", "Notebook", 60, 100, 12)
    store.add_product("P2", "Calculator", 850, 10, 18)
    store.add_product("P3", "Backpack", 1500, 6, 18)
    return store


def bill_summary(items):
    b = fresh().make_bill(items)
    return (b["subtotal"], b["discount"], b["gst"], b["total"])


def stock_after_bill():
    store = fresh()
    store.make_bill([("P1", 10)])
    return store.products["P1"]["stock"]


def stock_after_failed_bill():
    store = fresh()
    try:
        store.make_bill([("P1", 5), ("P3", 7)])      # P3 has only 6
    except Exception:
        pass
    return store.products["P1"]["stock"]             # must still be 100


def low_stock_after_sale():
    store = fresh()
    store.make_bill([("P3", 3)])                     # Backpack stock 6 -> 3
    return store.low_stock()


CASES = [
    ("Bill: 10 x Notebook (no discount)", (600.0, 0.0, 72.0, 672.0),
     lambda: bill_summary([("P1", 10)])),
    ("Bill: 3 x Calculator (5% discount slab)", (2550.0, 127.5, 436.05, 2858.55),
     lambda: bill_summary([("P2", 3)])),
    ("Bill: 4 x Backpack (10% discount slab)", (6000.0, 600.0, 972.0, 6372.0),
     lambda: bill_summary([("P3", 4)])),
    ("Discount rate for Rs.1999.99", 0.0, lambda: Store.discount_rate(1999.99)),
    ("Discount rate for Rs.2000", 0.05, lambda: Store.discount_rate(2000)),
    ("Discount rate for Rs.4999.99", 0.05, lambda: Store.discount_rate(4999.99)),
    ("Discount rate for Rs.5000", 0.10, lambda: Store.discount_rate(5000)),
    ("Notebook stock after selling 10", 90, stock_after_bill),
    ("Ask for more than the stock (7 Backpacks)",
     "Error: Insufficient stock for Backpack",
     lambda: fresh().make_bill([("P3", 7)])),
    ("Failed bill must not reduce stock of valid items", 100,
     stock_after_failed_bill),
    ("Unknown product code P9", "Error: Product not found: P9",
     lambda: fresh().make_bill([("P9", 1)])),
    ("Quantity 0", "Error: Quantity must be positive",
     lambda: fresh().make_bill([("P1", 0)])),
    ("Empty cart", "Error: Cart is empty", lambda: fresh().make_bill([])),
    ("Low-stock list after selling 3 Backpacks", ["Backpack"], low_stock_after_sale),
    ("Restock with negative quantity", "Error: Quantity must be positive",
     lambda: fresh().restock("P1", -5)),
    ("Add product with GST 40%", "Error: Invalid price, stock or GST rate",
     lambda: fresh().add_product("P4", "Bag", 100, 5, 40)),
]

if __name__ == "__main__":
    sys.exit(0 if run_cases(CASES) else 1)
