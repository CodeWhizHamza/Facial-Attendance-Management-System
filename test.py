import json

classesDone = {
    'day': 'monday',
    "0900": 0,
    "1000": 0,
    "1100": 0,
    "1200": 0,
    "1300": 0,
    "1400": 0,
    "1500": 0,
    "1600": 0,
    "1700": 0,
}

with open('attendanceRecord.json', 'w') as file:
    json.dump(classesDone, file)

# You marked attendance for 0900 class.
# classesDone['0900'] = 1

with open('attendanceRecord.json', 'w') as file:
    json.dump(classesDone, file)

with open('attendanceRecord.json', 'r') as file:
    previousRecord = json.load(file)
    print(previousRecord)
    currentTime = '0900'

    # if previousRecord['day'] != today:
    #     resetAttendanceRecord()

    if not previousRecord[currentTime]:
        # Start attendance
        print("Attendance started")
    else:
        print("Attendace for this class is already marked.")
