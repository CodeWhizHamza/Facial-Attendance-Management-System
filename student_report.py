import tkinter as tk
import customtkinter as ctk

from config import *
from helper import getAttendancePercentageFor, downloadReport, loadName, truncateWidget
import student_list


def studentReport(id, rightFrame):
    font40 = ctk.CTkFont('Arial', 40)
    font24 = ctk.CTkFont('Arial', 24)

    truncateWidget(rightFrame)

    emptyFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", height=120)
    emptyFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=80)
    rightHeaderFrame.pack(side=tk.TOP, fill=tk.X)

    studentName = loadName(id)
    rightHeaderLabel = tk.Label(
        master=rightHeaderFrame, text=f"{studentName}'s Attendance Report", font=font40, bg="#ffffff", fg="#333333", justify='left', anchor='w', wraplength=960)
    rightHeaderLabel.pack(fill=tk.X, side=tk.LEFT, padx=80)

    reportFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=640)
    reportFrame.pack(side=tk.TOP, fill=tk.X, padx=80, pady=64, anchor=tk.W)

    for index, course in enumerate(list(courses)):
        courseFrame = ctk.CTkFrame(
            master=reportFrame, bg_color="transparent", fg_color="transparent", width=960, height=80)
        courseFrame.pack(side=tk.TOP, fill=tk.X, anchor=tk.W)

        attendancePercentage = f'{getAttendancePercentageFor(id, course):.2f}%'
        courseLabel = tk.Label(
            master=courseFrame, text=f"{course} - {attendancePercentage}", font=font24, bg="#ffffff", fg="#333333", justify='left', anchor='w', wraplength=960)
        courseLabel.pack(fill=tk.X, side=tk.LEFT, padx=40, pady=4)

    detailsButton = tk.Button(master=rightFrame, text="Get Student report", font=font24, bg="#6FFD9D", fg="#333333", activebackground="#62E48C",
                              activeforeground="#333333", bd=0, highlightthickness=0, relief=tk.FLAT, padx=24, pady=12, command=lambda: downloadReport(id))
    detailsButton.pack(side=tk.TOP, padx=80, anchor=tk.W)

    # Back button
    backButton = tk.Button(master=rightFrame, text="Back",
                           font=font24, command=lambda: student_list.main(rightFrame), bg="#6FFD9D", fg="#333333", activebackground="#62E48C", activeforeground="#333333", bd=0, highlightthickness=0, relief=tk.FLAT, padx=64, pady=12)
    backButton.place(x=80, y=40)
