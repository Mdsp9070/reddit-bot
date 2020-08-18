from config import reddit
from collections import Counter
import csv

puncs = ':º-.,\n*;!?%$#(){}[]/\\\'\"'


def get_comments(url: str) -> list:
    comments: list = []
    sub = reddit.submission(url=url)
    sub.comments.replace_more(limit=None)

    for comment in sub.comments.list():
        comments.append(comment.body)

    return comments


def count(comments: str) -> list:
    for char in puncs:
        if char == '$' or char == '.':
            index = comments.index(char)
            if comments[index + 1].isdigit():
                continue
        comments = comments.replace(char, '')

    comments = comments.upper()

    words = comments.split()
    return Counter(words).most_common()


def generate_CSV(words_count: list):
    with open("words_count.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)

        for word_count in words_count:
            writer.writerow([word_count[0], word_count[1]])


def word_count(url: str) -> list:
    comments = get_comments(url)
    words_count = count(str(comments).strip('[]'))

    generate_CSV(words_count)

    return words_count
