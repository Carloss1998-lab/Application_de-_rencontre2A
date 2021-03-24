import re
import psycopg2
from dao.abstract_dao import AbstractDao
from collections import Counter
from string import punctuation
from math import sqrt

# initialize the connection to the database


cur = AbstractDao.connection.cursor()



def get_id(entityName, text):
    """Retrieve an entity's unique ID from the database, given its associated text.
    If the row is not already present, it is inserted.
    The entity can either be a sentence or a word."""
    tableName = entityName + 's'
    columnName = entityName
    cur.execute('SELECT rowid FROM ' + tableName + ' WHERE ' + columnName + ' = %s', (text,))
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        cur.execute('INSERT INTO ' + tableName + ' (' + columnName + ') VALUES (%s)', (text,))
        return cur.lastrowid

def get_words(text):
    """Retrieve the words present in a given string of text.
    The return value is a list of tuples where the first member is a lowercase word,
    and the second member the number of time it is present in the text."""
    wordsRegexpString = '(%s:\w+|[' + re.escape(punctuation) + ']+)'
    wordsRegexp = re.compile(wordsRegexpString)
    wordsList = wordsRegexp.findall(text.lower())
    return Counter(wordsList).items()


B = 'Hello!'
while True:
    # output bot's message
    print('B: ' + B)
    # ask for user input; if blank line, exit the loop
    H = input('H: ').strip()
    if H == '':
        break
    # store the association between the bot's message words and the user's response
    words = get_words(B)
    words_length = sum([n * len(word) for word, n in words])
    sentence_id = get_id('sentence', H)
    for word, n in words:
        word_id = get_id('word', word)
        weight = sqrt(n / float(words_length))
        cur.execute('INSERT INTO associations VALUES (%s, %s, %s)', (word_id, sentence_id, weight))
    AbstractDao.connection.commit()
    # retrieve the most likely answer from the database
    cur.execute('CREATE TEMPORARY TABLE results(sentence_id INT, sentence TEXT, weight REAL)')
    words = get_words(H)
    words_length = sum([n * len(word) for word, n in words])
    for word, n in words:
        weight = sqrt(n / float(words_length))
        cur.execute('INSERT INTO results SELECT associations.sentence_id, sentences.sentence, %s*associations.weight/(4+sentences.used) FROM words INNER JOIN associations ON associations.word_id=words.rowid INNER JOIN sentences ON sentences.rowid=associations.sentence_id WHERE words.word=%s', (weight, word,))
    # if matches were found, give the best one
    cur.execute('SELECT sentence_id, sentence, SUM(weight) AS sum_weight FROM results GROUP BY sentence_id ORDER BY sum_weight DESC LIMIT 1')
    row = cur.fetchone()
    cur.execute('DROP TABLE results')
    # otherwise, just randomly pick one of the least used sentences
    if row is None:
        cur.execute('SELECT rowid, sentence FROM sentences WHERE used = (SELECT MIN(used) FROM sentences) ORDER BY RANDOM() LIMIT 1')
        row = cur.fetchone()
    # tell the database the sentence has been used once more, and prepare the sentence
    B = row[1]
    cur.execute('UPDATE sentences SET used=used+1 WHERE rowid=%s', (row[0],))