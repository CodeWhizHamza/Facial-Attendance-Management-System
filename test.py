import sqlite3

from config import *


con = sqlite3.connect(databaseName)
cur = con.cursor()

query = ""
cur.execute(query)
con.commit()

cur.execute(f"SELECT (cmsId) FROM {tableName};")
studentsId = cur.fetchall()

for course in courses:
    query = f"""
        ALTER TABLE {course}
        DROP COLUMN `something`
    """
    cur.execute(query)
    con.commit()


cur.close()
con.close()
