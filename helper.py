from config import *
import sqlite3


def getAveragePercentage(id):
    # get percentage of every course
    # find average of that
    # return it
    percentageSum = 0
    for course in courses:
        percentageSum += getAttendancePercentageFor(id, course)
    return percentageSum / len(courses)


def printTable(table):
    con = sqlite3.connect(databaseName)
    cur = con.cursor()

    cur.execute(f"SELECT * FROM {tableName}")
    data = cur.fetchall()

    for id, name, semester in data:
        table.insert(parent='', index='end', iid=id, text='',
                     values=(id, name, semester, getAveragePercentage(id)))

    cur.close()
    con.close()


def getColumnNames(table: str):
    """
    This function get table name as argument.
    Then it returns user the list of columns which
    that table have.
    """
    con = sqlite3.connect(databaseName)
    cursor = con.cursor()

    cursor.execute(
        f"PRAGMA table_info({table});")
    columnNames = [n for _, n, *_ in cursor.fetchall()]

    cursor.close()
    con.close()

    return columnNames


def markAttendance(students: list, course: str, dayTime: str) -> None:
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


def getTotalNumberOfRecords(table):
    db = sqlite3.connect(databaseName)
    cursor = db.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM {table};")
    totalNumberOfRecords = cursor.fetchone()[0]

    cursor.close()
    db.close()
    return totalNumberOfRecords


def getAttendancePercentageFor(id: int, course: str) -> float:
    """This function will return percentage of presence of a student
    whose id is passed in the current course.

    Args:
        id (int): CMS ID of student
        course (str): Course code

    Returns:
        float: Percentage of attendance
    """
    course = course.upper()
    db = sqlite3.connect(databaseName)
    cursor = db.cursor()
    query = f"SELECT `{id}` FROM `{course}`;"
    cursor.execute(query)
    data = cursor.fetchall()
    # getting first item from the data returned from sql
    # That is either 'A' or 'P'
    data = [d for d, in data]
    cursor.close()
    db.close()

    totalRecordsCount = getTotalNumberOfRecords(course)
    presentCount = data.count('P')
    try:
        percentage = presentCount / totalRecordsCount * 100
    except ZeroDivisionError:
        return 0

    return percentage
