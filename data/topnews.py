import os
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import collections.abc
from collections import Counter
import sqlite3
from v1.v1.settings import BASE_DIR


def topnews():
    try:
        sqlite_connection = sqlite3.connect(os.path.join(BASE_DIR, 'recsys.sqlite3'))
        cursor = sqlite_connection.cursor()

        sqlite_select_query = """SELECT History from Behaviors"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        # raw_behaviour = pd.read_csv(
        #     "C:/Users/sasho/OneDrive/Рабочий стол/prog/recomend/RecSys/mind-news-dataset/MINDsmall_train/behaviors.tsv",
        #     sep="\t",
        #     names=["impressionId", "userId", "timestamp", "click_history", "impressions"])

        raw_behaviour = pd.DataFrame({'History': records})

        # clicks to rating news
        raw_behaviour = pd.DataFrame(raw_behaviour['History'].values.tolist(), index=raw_behaviour.index, columns=list(['History']))
        newsid = []
        newsid.extend(raw_behaviour['History'].str.split().to_list())
        cl2rat = []


        for sub in newsid:
            if not isinstance(sub, collections.abc.Sequence):
                continue
            for item  in sub:
                cl2rat.append(item)

        # top popular news
        cl2rat = list(Counter(cl2rat).items())

        for mydict in cl2rat:
            values = "'" + mydict[0] + "', " + str(mydict[1])
            sqlite_select_query = """INSERT INTO %s ( %s ) VALUES ( %s );""" % ('Top_news', 'id, CountOfClicks', values)
            print(sqlite_select_query)
            cursor.execute(sqlite_select_query)
            #sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


topnews()
