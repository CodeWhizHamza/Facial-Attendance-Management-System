import sqlite3
from tkinter.filedialog import asksaveasfile

from helper import getAttendanceTableFor
from config import *


def getReport():
    db = sqlite3.connect(databaseName)
    cursor = db.cursor()

    cursor.execute(f"SELECT `cmsId` FROM {tableName};")
    ids = [id for id, in cursor.fetchall()]
    files = [('Excel files', '*.xlsx'), ('All files', '*.*')]

    cursor.close()
    db.close()

    filename = asksaveasfile(
        filetypes=files, defaultextension=files, initialfile='class_attendance_record')
    if not filename:
        return

    filename = filename.name
    writer = pd.ExcelWriter(filename)
    for id in ids:
        attendanceTable = getAttendanceTableFor(id)
        attendanceTable.to_excel(writer, sheet_name=f'{id}', index=False)

    writer.close()
