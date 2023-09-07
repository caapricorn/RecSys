import os
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import collections.abc
from collections import Counter
import sqlite3
from recsystem.settings import BASE_DIR


def topnews():
    try:
        sqlite_connection = sqlite3.connect(os.path.join(BASE_DIR, 'recsys.sqlite3'))
        cursor = sqlite_connection.cursor()

        sqlite_select_query = """SELECT History from Behaviors"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        raw_behaviour = pd.DataFrame({'History': records})

        # clicks to rating news
        raw_behaviour = pd.DataFrame(raw_behaviour['History'].values.tolist(), index=raw_behaviour.index,
                                     columns=list(['History']))
        newsid = []
        newsid.extend(raw_behaviour['History'].str.split().to_list())
        cl2rat = []

        for sub in newsid:
            if not isinstance(sub, collections.abc.Sequence):
                continue
            for item in sub:
                cl2rat.append(item)

        # top popular news
        cl2rat = list(Counter(cl2rat).most_common())

        index = 1
        for mydict in cl2rat:
            values = str(index) + ", '" + mydict[0] + "', " + str(
                mydict[1]) + ", (SELECT Category FROM News WHERE id='" + mydict[0] + "')"
            sqlite_select_query = """INSERT INTO %s ( %s ) VALUES ( %s );""" % (
            'Top_news', 'id, NewsId, CountOfClicks, Category', values)
            print(sqlite_select_query)
            cursor.execute(sqlite_select_query)
            index += 1
            sqlite_connection.commit()

        index = 1
        for mydict in cl2rat[:16]:
            values = str(index) + ", (SELECT Category FROM News WHERE id='" + mydict[
                0] + "')" + ", (SELECT Title FROM News WHERE id='" + mydict[
                         0] + "')" + ", (SELECT Abstract FROM News WHERE id='" + mydict[0] + "')" + ", '" + mydict[0] + "'"
            sqlite_select_query = """INSERT INTO %s ( %s ) VALUES ( %s );""" % (
            'Main_news', 'id, Category, Title, Abstract, NewsId', values)
            cursor.execute(sqlite_select_query)
            index += 1
            sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def list_of_pop(category):
    try:
        sqlite_connection = sqlite3.connect(os.path.join(BASE_DIR, 'recsys.sqlite3'))
        cursor = sqlite_connection.cursor()

        value = ''
        for cat in category:
            value = value + "'" + cat + "'" + ', '

        sqlite_select_query = """SELECT * from Top_news WHERE Category IN ( %s )""" % value[:-2]
        print(sqlite_select_query)
        query = cursor.execute(sqlite_select_query)
        cols = [column[0] for column in query.description]
        personal_pop = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

        cursor.close()
        return personal_pop.head(10)
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()




topnews()
