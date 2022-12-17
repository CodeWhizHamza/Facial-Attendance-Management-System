import tkinter as tk
from tkinter import ttk
import sqlite3
import csv

from config import *
from helper import getAttendancePercentageFor, downloadReport, loadName


def studentReport(id):
    window = tk.Tk()
    window.title("Student Report")
    window.geometry('720x480')

    studentName = loadName(id)
    heading = tk.Label(master=window, text=f"{studentName}'s Attendance Report",
                       font='Arial 20 roman normal')
    heading.pack(pady=18)
    reportFrame = tk.Frame(master=window)
    reportFrame.pack()

    for index, course in enumerate(list(courses)):
        attendancePercentage = f'{getAttendancePercentageFor(id, course):.2f}%'
        courseName = tk.Label(master=reportFrame, text=f"{course}:", font=(
            "Arial, 16"))
        courseAttendance = tk.Label(master=reportFrame, text=attendancePercentage, font=(
            "Arial, 16"))
        courseName.grid(row=index, column=0, sticky=tk.E, padx=8)
        courseAttendance.grid(row=index, column=1, sticky=tk.W, padx=8)

    detailsButton = ttk.Button(
        master=window, text="Download detailed report", command=lambda: downloadReport(id))
    detailsButton.place(relx=0.15, rely=0.90)
    window.mainloop()
