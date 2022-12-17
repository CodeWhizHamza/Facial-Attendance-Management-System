import tkinter as tk
from tkinter import ttk
import sqlite3
import csv

from config import *
from helper import getAttendancePercentageFor, getAttendanceTableFor
from tkinter.filedialog import asksaveasfile


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

    def downloadReport():
        files = [('Excel files', '*.xlsx'), ('All files', '*.*')]
        attendanceReport = getAttendanceTableFor(id)
        filename = asksaveasfile(
            filetypes=files, defaultextension=files, initialfile=f'{id}')
        if filename:
            attendanceReport.to_excel(filename.name, index=False)

    loadData()
    heading = tk.Label(master=window, text=f"{studentName.get()}'s Attendance Report",
                       font='Arial 20 roman normal')
    heading.pack(pady=18)
    reportFrame = tk.Frame(master=window)
    reportFrame.pack()
    for index, course in enumerate(list(courses)):
        tk.Label(master=reportFrame, text=f"{course}:", font=(
            "Arial, 16")).grid(row=index, column=0, sticky=tk.E, padx=8)
        tk.Label(master=reportFrame, text=f'{getAttendancePercentageFor(id, course):.2f}%', font=(
            "Arial, 16")).grid(row=index, column=1, sticky=tk.W, padx=8)
    detailsButton = ttk.Button(
        master=window, text="Download detailed report", command=downloadReport)
    detailsButton.place(relx=0.15, rely=0.90)
    window.mainloop()
