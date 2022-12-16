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
title.grid(padx=8, pady=8)

buttonProperties = {
    'pady': 8,
    'padx': 26,
    'column': 0
}

buttonsFrame = ctk.CTkFrame(master=window, bg_color="transparent")
buttonsFrame.pack(padx=210, pady=48, expand=1, fill=tk.X)

getAttendanceReportButton = ctk.CTkButton(
    master=buttonsFrame, text="Get attendance report", width=250, font=font)
getAttendanceReportButton.grid(**buttonProperties)

addStudentButton = ctk.CTkButton(
    master=buttonsFrame, text="Add student", font=font, width=250, command=add_student.main)
addStudentButton.grid(**buttonProperties)

showAllStudentsButton = ctk.CTkButton(
    master=buttonsFrame, text="Show All students", width=250, font=font, command=student_list.main)
showAllStudentsButton.grid(**buttonProperties)

initializeSystem = ctk.CTkButton(
    master=buttonsFrame, text="Initialize System", width=250, font=font, command=attendance.main)
initializeSystem.grid(**buttonProperties)

window.mainloop()
