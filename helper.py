from config import *
import sqlite3


def printTable(table):
    con = sqlite3.connect(databaseName)
    cur = con.cursor()
    con.commit()

    cur.execute(f"SELECT * FROM {tableName}")
    data = cur.fetchall()

    for id, name, semester in data:
        table.insert(parent='', index='end', iid=id, text='',
                     values=(id, name, semester, 80))
