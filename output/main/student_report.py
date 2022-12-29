import tkinter as tk
import customtkinter as ctk

from config import *
from helper import getAttendancePercentageFor, downloadReport, loadName


def studentReport(id):
    window = ctk.CTkToplevel()
    window.title("Student Report")
    window.geometry('720x480')
    window.iconbitmap('resources/logo.ico')
    window.resizable(width=False, height=False)
    window.focus()

    studentName = loadName(id)
    heading = ctk.CTkLabel(master=window, text=f"{studentName}'s Attendance Report",
                           font=ctk.CTkFont('Arial', size=24))
    heading.pack(pady=24)
    reportFrame = tk.Frame(master=window)
    reportFrame.pack()

    font16 = ctk.CTkFont('Arial', size=16)

    for index, course in enumerate(list(courses)):
        attendancePercentage = f'{getAttendancePercentageFor(id, course):.2f}%'
        courseName = ctk.CTkLabel(
            master=reportFrame, text=f"{course}:", font=font16)
        courseAttendance = ctk.CTkLabel(
            master=reportFrame, text=attendancePercentage, font=font16)
        courseName.grid(row=index, column=0, sticky=tk.E, padx=8)
        courseAttendance.grid(row=index, column=1, sticky=tk.W, padx=8)

    detailsButton = ctk.CTkButton(
        master=window, text="Download detailed report", command=lambda: downloadReport(id))
    detailsButton.place(relx=0.10, rely=0.90)
    window.mainloop()
