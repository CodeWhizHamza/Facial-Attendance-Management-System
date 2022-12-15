import sqlite3
from config import *
from helper import getColumnNames

cs110 = {
    "15-12-2022-900": {
        "407251": 'P',
        "368494": 'A',
        "429551": 'P'
    },
    "15-12-2022-1000": {
        "407251": 'P',
        "368494": 'A',
        "429551": 'P'
    },
    "16-12-2022-900": {
        "407251": 'P',
        "368494": 'A',
        "429551": 'A'
    }
}


def getAttendencePercentageFor(id, course):
    course = course.upper()

    db = sqlite3.connect(databaseName)
    cursor = db.cursor()

    query = f"SELECT '{id}' FROM `{course}`;"
    cursor.execute(query)
    data = cursor.fetchall()

    print(data)

    cursor.close()
    db.close()

    # totalClasses = len(cs110.keys())
    # presentCount = 0

    # for _, report in cs110.items():
    #     if report[id] == 'P':
    #         presentCount += 1

    # return presentCount / totalClasses * 100
