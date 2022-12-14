import tkinter as tk

import add_student
import attendance
import student_list

window = tk.Tk()
window.title("HAM system")
window.resizable(width=False, height=False)
window.geometry('600x400')

titleFrame = tk.Frame(master=window)
titleFrame.grid(pady=20)

title = tk.Label(
    master=titleFrame, text="ATTENDANCE MANAGEMENT SYSTEM", fg='#333', font='Arial 23 roman bold')
title.pack()

buttonsFrame = tk.Frame(master=window)
buttonsFrame.grid(pady=48)

getAttendanceReportButton = tk.Button(
    master=buttonsFrame, text="Get attendance report", font="Arial 18 roman normal", width=30)
getAttendanceReportButton.pack(pady=8)

addStudentButton = tk.Button(
    master=buttonsFrame, text="Add student", font="Arial 18 roman normal", width=30, command=add_student.main)
addStudentButton.pack(pady=8)

showAllStudentsButton = tk.Button(
    master=buttonsFrame, text="Show All students", font="Arial 18 roman normal", width=30, command=student_list.main)
showAllStudentsButton.pack(pady=8)

initializeSystem = tk.Button(
    master=buttonsFrame, text="Initialize System", font="Arial 18 roman normal", width=30, command=attendance.main)
initializeSystem.pack(pady=8)

window.mainloop()
