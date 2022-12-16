import tkinter as tk
import customtkinter as ctk

import add_student
import attendance
import student_list


window = ctk.CTk()
window.title("HAM system")
window.resizable(width=False, height=False)
window.geometry('720x480')

font = ctk.CTkFont(family="Arial", size=20)

titleFrame = ctk.CTkFrame(master=window)
titleFrame.pack(pady=20)

title = ctk.CTkLabel(
    master=titleFrame, text="ATTENDANCE MANAGEMENT SYSTEM", font=font)
title.grid()

buttonsFrame = ctk.CTkFrame(master=window, bg_color="transparent")
buttonsFrame.pack(padx=100, pady=48, expand=1, fill=tk.X)

getAttendanceReportButton = ctk.CTkButton(
    master=buttonsFrame, text="Get attendance report",  width=30, font=font)
getAttendanceReportButton.grid(pady=8)

addStudentButton = ctk.CTkButton(
    master=buttonsFrame, text="Add student",  width=30, font=font, command=add_student.main)
addStudentButton.grid(pady=8)

showAllStudentsButton = ctk.CTkButton(
    master=buttonsFrame, text="Show All students",  width=30, font=font, command=student_list.main)
showAllStudentsButton.grid(pady=8)

initializeSystem = ctk.CTkButton(
    master=buttonsFrame, text="Initialize System",  width=30, font=font, command=attendance.main)
initializeSystem.grid(pady=8)

window.mainloop()
