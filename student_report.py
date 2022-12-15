import tkinter as tk
from tkinter import ttk
import sqlite3

from config import *


def studentReport(id, table):
    window = tk.Tk()
    window.title("Student Report")
    window.geometry('720x480')

    studentId = tk.IntVar()
    studentName = tk.StringVar()
    studentSemester = tk.IntVar()

    def loadData():
        db = sqlite3.connect(databaseName)
        cursor = db.cursor()

        query = f"SELECT * FROM {tableName} WHERE cmsId={id}"
        cursor.execute(query)
        cmsId, name, semester = cursor.fetchall()[0]
        studentId.set(cmsId)
        studentName.set(name)
        studentSemester.set(semester)

        cursor.close()
    loadData()
    heading = tk.Label(master=window, text=f"{studentName.get()}'s Report",
                       font='Arial 24 roman normal')
    heading.pack(pady=18)
    window.mainloop()
