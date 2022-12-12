import sqlite3
con = sqlite3.connect('db.sqlite')
cur = con.cursor()


query = "CREATE TABLE IF NOT EXISTS students('CMS ID' INTEGER PRIMARY KEY AUTOINCREMENT, 'name' TEXT, 'semester' TEXT);"
cur.execute(query)
con.commit()

cur.close()
con.close()
