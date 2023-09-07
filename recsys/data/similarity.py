import os
import sqlite3

from django.conf import settings

import recsys.data.corr as corr
import recsys.data.topnews as top

def similar(id):
    try:
        sqlite_connection = sqlite3.connect(os.path.join(settings.BASE_DIR, 'recsys.sqlite3'))
        cursor = sqlite_connection.cursor()
        value = "'" + id + "'"
        sqlite_select_query = """SELECT Category from News WHERE id= %s """ % (value)
        cursor.execute(sqlite_select_query)
        category = cursor.fetchone()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

    max_values = corr.matrix[category[0]].sort_values(ascending=False)[1:4]
    print(top.list_of_pop(max_values.index.to_list()))