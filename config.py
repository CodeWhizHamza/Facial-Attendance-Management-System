import pandas as pd

"""This file contains all the configuration variables."""

databaseName = "db.sqlite"
tableName = "students"
directoryName = "known_encodings"

timeTable = {
    "0900": ["MATH161", None, "CS110lab", "CS110", "CS110"],
    "1000": ["MATH111", None, "CS110lab", "CS110", "HU107"],
    "1100": ["HU108", "MATH111", "CS110lab", "MATH111", "CS100"],
    "1200": ["HU108", "CS100", "MATH161", "MATH111", None],
    "1300": [None, None, None, None, None],
    "1400": [None, "CS100lab", "HU108", None, None],
    "1500": [None, "CS100lab", None, "HU107", None],
    "1600": [None, "CS100lab", None, None, None]
}

timeTable = pd.DataFrame(
    timeTable, index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])


courses = list()
for item in timeTable.values:
    for i in item:
        if i is None or i in courses:
            continue
        courses.append(i)


password = "admin"
