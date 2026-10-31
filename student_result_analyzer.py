"""
Case Study 3: Student Result Analyzer
-------------------------------------
Takes marks of students in 5 subjects and produces total, percentage, grade,
pass/fail result, rank (ties share a rank) and class statistics
(average, standard deviation, pass percentage, subject toppers).

Run:  python student_result_analyzer.py          -> enter your own data
      python student_result_analyzer.py --demo   -> automatic sample run
"""
import sys

SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Python"]
PASS_MARK = 40       # minimum marks needed in EACH subject


def calculate_grade(percentage):
    """Convert a percentage into a letter grade."""
    if percentage >= 90:
        return "O"
    if percentage >= 80:
        return "A+"
    if percentage >= 70:
        return "A"
    if percentage >= 60:
        return "B"
    if percentage >= 50:
        return "C"
    if percentage >= 40:
        return "P"
    return "F"


def validate_marks(marks):
    """Marks list must have one mark (0-100) for every subject."""
    if len(marks) != len(SUBJECTS):
        raise ValueError("Exactly " + str(len(SUBJECTS)) + " marks are required")
    for m in marks:
        if not isinstance(m, (int, float)) or m < 0 or m > 100:
            raise ValueError("Marks must be between 0 and 100")


def analyse(students):
    """
    students: dict  name -> list of marks.
    Returns a list of result records sorted by rank.
    """
    records = []
    for name, marks in students.items():
        validate_marks(marks)
        total = sum(marks)
        percentage = round(total / len(marks), 2)   # each subject is out of 100
        # a student passes only if every subject is at least PASS_MARK
        result = "PASS" if min(marks) >= PASS_MARK else "FAIL"
        grade = calculate_grade(percentage) if result == "PASS" else "F"
        records.append({"name": name, "marks": marks, "total": total,
                        "percentage": percentage, "grade": grade,
                        "result": result})

    # highest total first; equal totals get the same rank (1,2,2,4 style)
    records.sort(key=lambda r: (-r["total"], r["name"]))
    for i, rec in enumerate(records):
        if i > 0 and rec["total"] == records[i - 1]["total"]:
            rec["rank"] = records[i - 1]["rank"]
        else:
            rec["rank"] = i + 1
    return records


def class_statistics(records):
    """Average, standard deviation, pass percentage and toppers."""
    n = len(records)
    totals = [r["total"] for r in records]
    average = sum(totals) / n
    variance = sum((t - average) ** 2 for t in totals) / n
    passed = sum(1 for r in records if r["result"] == "PASS")
    topper_total = max(totals)
    subject_toppers = {}
    for index, subject in enumerate(SUBJECTS):
        best = max(r["marks"][index] for r in records)
        names = [r["name"] for r in records if r["marks"][index] == best]
        subject_toppers[subject] = (best, names)
    return {
        "average": round(average, 2),
        "std_dev": round(variance ** 0.5, 2),
        "pass_percentage": round(passed * 100 / n, 2),
        "toppers": [r["name"] for r in records if r["total"] == topper_total],
        "subject_toppers": subject_toppers,
    }


def print_report(records):
    print(f"{'Rank':<5}{'Name':<10}{'Total':>6}{'%':>8}{'Grade':>7}{'Result':>8}")
    for r in records:
        print(f"{r['rank']:<5}{r['name']:<10}{r['total']:>6}"
              f"{r['percentage']:>8}{r['grade']:>7}{r['result']:>8}")
    stats = class_statistics(records)
    print("\nClass average      :", stats["average"])
    print("Standard deviation :", stats["std_dev"])
    print("Pass percentage    :", stats["pass_percentage"], "%")
    print("Topper(s)          :", ", ".join(stats["toppers"]))
    for subject, (best, names) in stats["subject_toppers"].items():
        print(f"Highest in {subject:<10}: {best} ({', '.join(names)})")


def demo():
    students = {
        "Anil":   [92, 88, 95, 85, 98],
        "Bhavya": [78, 82, 75, 80, 85],
        "Charan": [35, 60, 55, 70, 65],     # fails Maths
        "Divya":  [92, 88, 95, 85, 98],     # same marks as Anil (tie)
        "Esha":   [60, 55, 58, 62, 70],
    }
    print_report(analyse(students))


def main():
    students = {}
    count = int(input("Number of students: "))
    for _ in range(count):
        name = input("Student name: ")
        marks = [float(input("  " + s + ": ")) for s in SUBJECTS]
        students[name] = marks
    try:
        print_report(analyse(students))
    except ValueError as err:
        print("Error:", err)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else main()
