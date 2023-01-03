"""
Part by: Muhammad Hamza
"""

import sqlite3
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
import os

from helper import getAttendanceTableFor
from config import *


def getReport():
    """This function will download the attendance report of a student"""

    # If no students are added, then show warning and return
    if not os.path.exists("./known_encodings"):
        messagebox.showwarning(
            "Warning", "No students found. Please add students and mark their attendance first.")
        return

    # If no students are added, then show warning and return
    if len(os.listdir("./known_encodings")) == 0:
        messagebox.showwarning(
            "Warning", "No students found. Please add students and mark their attendance first.")
        return

    db = sqlite3.connect(databaseName)
    cursor = db.cursor()

    cursor.execute(f"SELECT `cmsId` FROM {tableName};")
    ids = [id for id, in cursor.fetchall()]
    files = [('Excel files', '*.xlsx'), ('All files', '*.*')]

    cursor.close()
    db.close()

    # Ask user for filename and location
    filename = asksaveasfile(
        filetypes=files, defaultextension=files, initialfile='class_attendance_record')
    if not filename:
        return

    # write data to excel file
    filename = filename.name
    writer = pd.ExcelWriter(filename)
    for id in ids:
        attendanceTable = getAttendanceTableFor(id)
        attendanceTable.to_excel(writer, sheet_name=f'{id}', index=False)

    writer.close()
