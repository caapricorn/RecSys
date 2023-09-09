import os
import sqlite3

import pandas as pd
import recsys.data.corr as corr
import recsys.data.topnews as top
import recsys.data.cosine_similarity as cos

from django.conf import settings


def similar(id):
    try:
        sqlite_connection = sqlite3.connect(os.path.join(settings.BASE_DIR, 'recsys.sqlite3'))
        cursor = sqlite_connection.cursor()
        value = "'" + id + "'"
        sqlite_select_query = """SELECT Category from News WHERE id= %s """ % value
        cursor.execute(sqlite_select_query)
        category = cursor.fetchone()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

    max_values = corr.matrix[category[0]].sort_values(ascending=False)[1:4]
    top_of_pop_similar = top.list_of_pop(max_values.index.to_list(), category[0])
    top_of_pop_similar = top_of_pop_similar.set_index("NewsId").drop([id])
    top_of_pop_similar.reset_index(inplace=True)
    similar_news = cos.cos_top(top_of_pop_similar, id)

    try:
        sqlite_connection = sqlite3.connect(os.path.join(settings.BASE_DIR, 'recsys.sqlite3'))
        cursor = sqlite_connection.cursor()
        value = ''
        for id_top in similar_news:
            value = value + "'" + id_top + "'" + ', '
        sqlite_select_query = """SELECT * from News WHERE id IN ( %s ) """ % value[:-2]
        query = cursor.execute(sqlite_select_query)
        cols = [column[0] for column in query.description]
        similar_news = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

    return similar_news
