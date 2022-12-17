import tkinter as tk
import customtkinter as ctk
from PIL import Image

import add_student
import attendance
import student_list

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

window = ctk.CTk()
window.title("AMS")
window.resizable(width=False, height=False)
window.geometry('720x480')
window.iconbitmap('resources/logo.ico')

font = ctk.CTkFont(family="Arial", size=20)
font16 = ctk.CTkFont(family="Arial", size=16)

titleFrame = ctk.CTkFrame(
    master=window, bg_color="transparent", fg_color="transparent")
titleFrame.pack(pady=16)

titleImage = ctk.CTkLabel(
    titleFrame, image=ctk.CTkImage(light_image=Image.open('resources/logo.png'), dark_image=Image.open('resources/logo.png'), size=(160, 160)), text="")
titleImage.grid(row=0, column=0, sticky=tk.W)
title = ctk.CTkLabel(
    master=titleFrame, text="Attendance Management\nSystem", font=font16, anchor=tk.W, justify='left')
title.grid(pady=8, row=0, column=1, sticky=tk.E)


buttonProperties = {
    'pady': 8,
    'padx': 26,
    'column': 0
}

buttonsFrame = ctk.CTkFrame(master=window, bg_color="transparent")
buttonsFrame.pack(padx=210, pady=0, fill=tk.X)

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
