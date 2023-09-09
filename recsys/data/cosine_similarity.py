import os
import sqlite3
import pandas as pd
import re

from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recsystem.settings import BASE_DIR


def cos():
    try:
        sqlite_connection = sqlite3.connect(os.path.join(BASE_DIR, 'recsys.sqlite3'))
        cursor = sqlite_connection.cursor()

        sqlite_select_query = """SELECT Title from News"""
        query = cursor.execute(sqlite_select_query)
        cols = [column[0] for column in query.description]
        news = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

        cursor.close()

    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

    # remove unnecessary punctuation marks from text
    corpus = news['Title'].str.lower().values
    corpus_new = []
    for text in corpus:
        text = re.sub(r'\xa0', ' ', text)
        text = re.sub(r'«»,:', '', text)
        corpus_new.append(text)

    # Create an instance of the tokenizer
    tokenizer = Tokenizer(num_words=1000)

    # The tokenizer updates the token dictionary according to the frequency of occurrence of words
    tokenizer.fit_on_texts(corpus_new)

    # List all words in a dictionary
    word_indexes = tokenizer.word_index
    word_indexes[',,'] = 0

    # Let's get the numeric representation of the text
    tokenizer.texts_to_sequences(corpus_new)
    vectorizer = CountVectorizer(vocabulary=word_indexes)
    sentence_vectors = vectorizer.fit_transform(corpus_new)
    cosine_similarities = cosine_similarity(sentence_vectors, sentence_vectors[:1])
    print(cosine_similarities)


def cos_top(top_of_pop_similar, id):
    try:
        sqlite_connection = sqlite3.connect(os.path.join(BASE_DIR, 'recsys.sqlite3'))
        cursor = sqlite_connection.cursor()

        value = ''
        for id_top in top_of_pop_similar.iterrows():
            value = value + "'" + str(id_top[1]["NewsId"]) + "'" + ', '

        sqlite_select_query = """SELECT Title from News WHERE id IN ( %s )""" % value[:-2]
        query = cursor.execute(sqlite_select_query)
        cols = [column[0] for column in query.description]
        news = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

        value = "'" + id + "'"

        sqlite_select_query = """SELECT Title from News WHERE id IN ( %s )""" % value
        query = cursor.execute(sqlite_select_query)
        news.loc[len(news.index)] = query.fetchone()

        cursor.close()

    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

    # remove unnecessary punctuation marks from text
    corpus = news['Title'].str.lower().values
    corpus_new = []
    for text in corpus:
        text = re.sub(r'\xa0', ' ', text)
        text = re.sub(r'«»,:', '', text)
        corpus_new.append(text)

    # Create an instance of the tokenizer
    tokenizer = Tokenizer(num_words=1000)

    # The tokenizer updates the token dictionary according to the frequency of occurrence of words
    tokenizer.fit_on_texts(corpus_new)

    # List all words in a dictionary
    word_indexes = tokenizer.word_index
    word_indexes[',,'] = 0

    # Let's get the numeric representation of the text
    tokenizer.texts_to_sequences(corpus_new)
    vectorizer = CountVectorizer(vocabulary=word_indexes)
    sentence_vectors = vectorizer.fit_transform(corpus_new)
    cosine_similarities = cosine_similarity(sentence_vectors, sentence_vectors[-1])
    print(cosine_similarities)
    x = 0
    index = []
    for article in cosine_similarities:
        if (article[0]) > 0.001 and (1.0 - article[0]) > 0.001:
            index.append(top_of_pop_similar.iloc[x]["NewsId"])
        x += 1
    if not index:
        for i in range(3):
            index.append(top_of_pop_similar.iloc[i]["NewsId"])
    return index

cos()