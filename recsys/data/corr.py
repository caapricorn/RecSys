import os
import sqlite3
import pandas as pd

from collections import Counter
from v1.recsystem.settings import BASE_DIR

a = 45

# Index click history field
def corr():

    try:
        sqlite_connection = sqlite3.connect(os.path.join(BASE_DIR, 'recsys.sqlite3'))
        cursor = sqlite_connection.cursor()

        sqlite_select_query = """SELECT UserId, History from Behaviors"""

        query = cursor.execute(sqlite_select_query)
        cols = [column[0] for column in query.description]
        cl2cat = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

        sqlite_select_query = """SELECT id, Category from News"""
        query = cursor.execute(sqlite_select_query)
        cols = [column[0] for column in query.description]
        news = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

        cursor.close()

    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

    # Build index of items
    ind2item = {idx + 1: itemid for idx, itemid in enumerate(news['id'].values)}
    item2ind = {itemid: idx for idx, itemid in ind2item.items()}

    def click_history(s):

        list_of_strings = str(s).split(" ")
        return [news['Category'].get(item2ind.get(l, 0)) for l in list_of_strings]

    pd.options.mode.chained_assignment = None
    cl2cat['click_history_category'] = cl2cat.History.map(lambda s: click_history(s))

    cl2cat['counter_category'] = cl2cat.click_history_category.map(lambda s: Counter(s))

    usercat = cl2cat[['UserId', 'click_history_category']]

    agg_function = {'UserId': 'first', 'click_history_category': 'sum'}
    unique_usercat = usercat.groupby(usercat['UserId']).aggregate(agg_function)

    unique_usercat['counter_category'] = unique_usercat.click_history_category.map(lambda s: Counter(s))
    matrix = pd.DataFrame.from_records(unique_usercat['counter_category'])
    return matrix.corr()


matrix = corr()