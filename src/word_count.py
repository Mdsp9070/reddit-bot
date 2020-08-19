import csv
import re
from config import reddit
from collections import Counter

# define punctuation constant to remove
puncs = ':º-.,\n*;!?%$#(){}[]/\\\"'

# get all comments from reddit thread


def get_comments(url: str) -> list:
    comments: list = []
    sub = reddit.submission(url=url)
    sub.comments.replace_more(limit=None)

    for comment in sub.comments.list():
        comments.append(comment.body)

    return comments


# count each occurence of a word into comments array
def count_words(comments: str) -> list:
    # remove links
    comments = re.sub(r'http\S+', '', comments, flags=re.MULTILINE)

    # remove punctuation and digits
    for char in puncs:
        comments = comments.replace(char, '')

    for word in comments.split():
        if word.isdigit():
            comments = comments.replace(word, '')

    comments = comments.upper()

    words = comments.split()
    return Counter(words).most_common()

# generate a CSV with two columns: the word and it's count


def generate_CSV(words_count: list):
    with open("words_count.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)

        for word_count in words_count:
            writer.writerow([word_count[0], word_count[1]])


# calls all helper funtions
def word_count(url: str) -> list:
    comments = get_comments(url)
    words_count = count_words(str(comments).strip('[]'))

    generate_CSV(words_count)

    return words_count
