"""Test cases for Case Study 5 (Text Analyzer).
Run:  python test_text_analyzer.py           -> readable results
      python test_text_analyzer.py --table   -> Markdown table for the report
"""
import sys
from text_analyzer import (analyse, average_word_length, count_sentences, get_words,
                           is_pangram, longest_word, palindromes,
                           vowel_consonant_count, word_frequency)


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


def full_summary():
    r = analyse("One two three.")
    return (r["words"], r["sentences"], r["longest_word"])


CASES = [
    ("Words of \"Hello, World! It's 5 PM\"", ["hello", "world", "it's", "pm"],
     lambda: get_words("Hello, World! It's 5 PM")),
    ("Sentences in \"Hi. How are you? Fine!\"", 3,
     lambda: count_sentences("Hi. How are you? Fine!")),
    ("Sentences in \"No end\" (no punctuation)", 1, lambda: count_sentences("No end")),
    ("Sentences in \"...\"", 0, lambda: count_sentences("...")),
    ("Top 2 words of \"a b a c b a\"", [("a", 3), ("b", 2)],
     lambda: word_frequency("a b a c b a", 2)),
    ("Equal counts sorted alphabetically", [("apple", 2), ("pear", 2)],
     lambda: word_frequency("pear apple pear apple", 2)),
    ("Longest word of \"I love programming\"", "programming",
     lambda: longest_word("I love programming")),
    ("Longest word of empty text", "", lambda: longest_word("")),
    ("Vowels/consonants of \"Hello World 123\"", (3, 7),
     lambda: vowel_consonant_count("Hello World 123")),
    ("Palindromes in \"Madam Anna saw a level civic noon\"",
     ["anna", "civic", "level", "madam", "noon"],
     lambda: palindromes("Madam Anna saw a level civic noon")),
    ("Single-letter words are not palindromes", [], lambda: palindromes("a I x")),
    ("Pangram: quick brown fox sentence", True,
     lambda: is_pangram("The quick brown fox jumps over the lazy dog")),
    ("Pangram: \"Hello world\"", False, lambda: is_pangram("Hello world")),
    ("Average word length of \"ab abcd\"", 3.0, lambda: average_word_length("ab abcd")),
    ("Full analysis of \"One two three.\" (words, sentences, longest)",
     (3, 1, "three"), full_summary),
    ("Empty text", "Error: Text is empty", lambda: analyse("")),
    ("Only spaces", "Error: Text is empty", lambda: analyse("    ")),
]

if __name__ == "__main__":
    sys.exit(0 if run_cases(CASES) else 1)
