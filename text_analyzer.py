"""
Case Study 5: Text Analyzer
---------------------------
Analyses a paragraph: word / sentence count, word frequency, longest word,
vowels and consonants, palindrome words, pangram check, average word length.

Run:  python text_analyzer.py          -> type or paste your own text
      python text_analyzer.py --demo   -> automatic sample run
"""
import re
import string
import sys


def get_words(text):
    """Return all words in lower case (letters and apostrophes only)."""
    return re.findall(r"[a-z']+", text.lower())


def count_sentences(text):
    """A sentence ends with . ! or ?  Empty pieces are ignored."""
    pieces = re.split(r"[.!?]+", text)
    return len([p for p in pieces if p.strip()])


def word_frequency(text, top_n=5):
    """Most common words as (word, count), highest first, ties alphabetical."""
    counts = {}
    for word in get_words(text):
        counts[word] = counts.get(word, 0) + 1
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    return ranked[:top_n]


def longest_word(text):
    """First longest word; empty string if there are no words."""
    best = ""
    for word in get_words(text):
        if len(word) > len(best):
            best = word
    return best


def vowel_consonant_count(text):
    vowels = consonants = 0
    for ch in text.lower():
        if ch in "aeiou":
            vowels += 1
        elif ch in string.ascii_lowercase:
            consonants += 1
    return vowels, consonants


def palindromes(text):
    """Unique palindrome words with at least 3 letters, sorted."""
    found = set()
    for word in get_words(text):
        if len(word) >= 3 and word == word[::-1]:
            found.add(word)
    return sorted(found)


def is_pangram(text):
    """True if every letter a-z appears at least once."""
    letters = set(ch for ch in text.lower() if ch in string.ascii_lowercase)
    return len(letters) == 26


def average_word_length(text):
    words = get_words(text)
    if not words:
        return 0
    return round(sum(len(w) for w in words) / len(words), 2)


def analyse(text):
    if not text.strip():
        raise ValueError("Text is empty")
    vowels, consonants = vowel_consonant_count(text)
    return {
        "words": len(get_words(text)),
        "sentences": count_sentences(text),
        "top_words": word_frequency(text),
        "longest_word": longest_word(text),
        "vowels": vowels,
        "consonants": consonants,
        "palindromes": palindromes(text),
        "pangram": is_pangram(text),
        "avg_word_length": average_word_length(text),
    }


def show(result):
    for key, value in result.items():
        print(f"{key:<16}: {value}")


def demo():
    text = ("The quick brown fox jumps over the lazy dog. "
            "Madam saw a level road near the civic centre! "
            "Is the dog lazy or is the fox quick?")
    print("Text:", text, "\n")
    show(analyse(text))


def main():
    text = input("Enter your text: ")
    try:
        show(analyse(text))
    except ValueError as err:
        print("Error:", err)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else main()
