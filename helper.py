from config import *
import sqlite3


def printTable(table):
    con = sqlite3.connect(databaseName)
    cur = con.cursor()

    cur.execute(f"SELECT * FROM {tableName}")
    data = cur.fetchall()

    for id, name, semester in data:
        table.insert(parent='', index='end', iid=id, text='',
                     values=(id, name, semester, 80))

    cur.close()
    con.close()


def getColumnNames(table):
    con = sqlite3.connect(databaseName)
    cursor = con.cursor()

    cursor.execute(
        f"PRAGMA table_info({table});")
    columnNames = [n for _, n, *_ in cursor.fetchall()]

    cursor.close()
    con.close()

    return columnNames


def markAttendence(students: list, course: str, dayTime: str) -> None:
    """
    This function accepts a list of student ids which are supposed to
    be marked as present.
    Second argument is the course for which this attendance is to be
    marked.
    Third is the unique Identifier for this day and this time of this 
    class.
    """
    course = course.upper()
    columns = getColumnNames(course)

    db = sqlite3.connect(databaseName)
    cursor = db.cursor()

    columnsString = ["dayTime"]
    valuesString = [f"'{dayTime}'"]
    for column in columns[1:]:
        if column in students:
            columnsString.append(f"'{column}'")
            valuesString.append("'P'")
        else:
            columnsString.append(f"'{column}'")
            valuesString.append("'A'")

    columnsString = ", ".join(columnsString)
    valuesString = ",".join(valuesString)

    query = f"INSERT INTO {course} ({columnsString}) VALUES ({valuesString});"
    cursor.execute(query)
    db.commit()

    cursor.close()
    db.close()
