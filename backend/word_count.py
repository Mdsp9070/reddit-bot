import csv
import re
import os
import requests
import pathlib
import re
from time import sleep
from collections import Counter

# define punctuation constant to remove
puncs = ':º-.,\n*;!?%$#(){}[]/\\\"\'\n\t'


def get_sub_id(url: str) -> str:
    url = url.split('/')

    if 'comments' not in url:
        sub_id = url[url.index('redd.it') + 1]
        if 'r' in url:
            return ''
    else:
        sub_id = url[url.index('comments') + 1]

    return sub_id

# get all comments from reddit thread


def get_comments(sub_id: str) -> list:
    url = f'https://api.pushshift.io/reddit/submission/comment_ids/{sub_id}'
    req = requests.get(url)
    print(url)
    sub = req.json()

    comments_ids = []
    for id in sub['data']:
        comments_ids.append(id)

    comments_list = []
    while len(comments_ids) > 0:
        req = requests.get(
            f'https://api.pushshift.io/reddit/comment/search?ids={",".join(comments_ids[:1000])}')

        comments_data = req.json()

        for comment in comments_data['data']:
            comments_list.append(comment['body'])

        del comments_ids[:1000]

    return comments_list


# def get_comments(url: str) -> list:
#     sub = reddit.submission(url=url)

#     while True:
#         try:
#             sub.comments.replace_more(limit=None, threshold=0)
#             break
#         except RequestException:
#             sleep(1)
#             continue

#     comments: list = []
#     for comment in sub.comments.list():
#         if isinstance(comment, MoreComments):
#             continue
#         comments.append(comment.body)

#     return comments

def deEmojify(text: str) -> str:
    regrex_pattern = re.compile(pattern="["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)

# count each occurence of a word into comments array


def count_words(comments: str, filter: list = [], uppercase: bool = False) -> list:
    # remove links
    comments = re.sub(r'http\S+', '', comments, flags=re.MULTILINE)

    # remove invalid ascii characters
    comments = deEmojify(comments)

    # remove punctuation and digits
    for char in puncs:
        comments = comments.replace(char, '')

    for word in comments.split():
        if word.isdigit():
            comments = comments.replace(word, '')

    # if uppercase only was checked
    # return only words which is upper
    if uppercase:
        uppercased = []
        for word in comments.split():
            if word.isupper():
                uppercased.append(word)
        return Counter(uppercased).most_common()

    # remove words from filter
    comments = comments.upper()
    if len(filter) > 0:
        for word in filter:
            word = word.upper()
            comments = comments.replace(word, '')

    words = comments.split()
    return Counter(words).most_common()


# generate a CSV with two columns: the word and it's count
def generate_CSV(words_count: list):
    folderpath = pathlib.Path(__file__).parent
    filepath = os.path.join(folderpath, './csv/words_count.csv')
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for word_count in words_count:
            writer.writerow([word_count[0], word_count[1]])


# calls all helper funtions
def word_count(url: str, filter: list, uppercase: bool) -> int:
    sub_id = get_sub_id(url)

    if not sub_id:
        return 1

    comments = get_comments(sub_id)

    words_count = count_words(str(comments).strip(
        '[]'), filter=filter, uppercase=uppercase)

    generate_CSV(words_count)

    return 0
