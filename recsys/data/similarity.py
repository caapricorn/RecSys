import os
import sqlite3

from django.conf import settings
#import corr

def similar(id):
    try:
        sqlite_connection = sqlite3.connect(os.path.join(settings.BASE_DIR, 'recsys.sqlite3'))
        cursor = sqlite_connection.cursor()
        value = "'" + id + "'"
        sqlite_select_query = """SELECT Category from News WHERE id= %s """ % (value)
        cursor.execute(sqlite_select_query)
        category = cursor.fetchone()
        print(category[0])
        #(corr.matrix)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()