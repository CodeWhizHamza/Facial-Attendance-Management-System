# import sqlite3

# con = sqlite3.connect('db.sqlite')
# cur = con.cursor()

# cur.execute("DELETE FROM MATH161;")
# con.commit()

# cur.execute('SELECT * FROM MATH161;')
# print(cur.fetchall())


# cur.close()
# con.close()

# # import json

# # # some JSON:
# # x = {"day": "Monday",
# #      "0900": 0,
# #      "1000": 0,
# #      "1100": 0,
# #      "1200": 0,
# #      "1300": 0,
# #      "1400": 0,
# #      "1500": 0,
# #      "1600": 0}

# # with open('attendanceVariables.json', 'w') as file:
# #     json.dump(x, file)

# # with open('attendanceVariables.json', 'r') as file:
# #     y = json.load(file)

# # # the result is a Python dictionary:
# # print(y["day"])
