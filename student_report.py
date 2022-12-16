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
    heading = tk.Label(master=window, text=f"{studentName.get()}'s Attendance Report",
                       font='Arial 20 roman normal')
    heading.pack(pady=18)
    reportFrame = tk.Frame(master=window)
    reportFrame.pack()
    for index, course in enumerate(list(courses)):
        a = tk.Label(master=reportFrame, text=f"{course}:", font=(
            "Arial, 16")).grid(row=index, column=0, sticky=tk.E, padx=8)
        b = tk.Label(master=reportFrame, text="80%", font=(
            "Arial, 16")).grid(row=index, column=1, sticky=tk.W, padx=8)
    detailsButton = ttk.Button(
        master=window, text="Download detailed report")
    detailsButton.place(relx=0.75, rely=0.90)
    window.mainloop()
