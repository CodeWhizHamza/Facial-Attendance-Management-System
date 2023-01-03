import tkinter as tk
import customtkinter as ctk
from PIL import Image


from getTotalAttendanceReport import getReport
from content import showContent


def showSidebar(root_window, active_button=None):
    font = ctk.CTkFont(family="Arial", size=20)

    # clear content of root window
    for widget in root_window.winfo_children():
        widget.destroy()

    def onAddStudentButtonPress():
        active_button = 'addStudentButton'
        showSidebar(root_window, active_button)
        # add_student.main(root_window)

    def onShowAllStudentsButtonPress():
        active_button = 'showAllStudentsButton'
        showSidebar(root_window, active_button)
        # student_list.main(root_window)

    def onInitializeSystemButtonPress():
        active_button = 'initializeSystem'
        showSidebar(root_window, active_button)
        # attendance.main(root_window)

    leftFrame = ctk.CTkFrame(master=root_window, bg_color="#f5f5f5", width=320)
    leftFrame.pack(side=tk.LEFT, fill=tk.Y)

    logoFrame = ctk.CTkFrame(
        master=leftFrame, bg_color="transparent", fg_color="transparent")
    logoFrame.pack(padx=24, pady=24, fill=tk.X)

    logoImage = ctk.CTkLabel(
        logoFrame, image=ctk.CTkImage(light_image=Image.open('resources/header.png'), dark_image=Image.open('resources/header.png'), size=(277, 77)), text="")
    logoImage.grid(row=0, column=0, sticky=tk.W)

    leftButtonsFrame = ctk.CTkFrame(
        master=leftFrame, bg_color="transparent", fg_color="transparent")
    leftButtonsFrame.pack(pady=16, fill=tk.BOTH, expand=True)

    buttonsConfig = {
        "addStudentButton": {
            "bg": "#ffffff" if active_button != 'addStudentButton' else "#6FFD9D",
            "fg": "#000000",
            "activebackground": "#ffffff" if active_button != 'addStudentButton' else "#62E48C",
            "activeforeground": "#000000",
            "highlightthickness": 0,
            "relief": tk.FLAT,
            "justify": tk.LEFT,
            "pady": 16
        },
        "showAllStudentsButton": {
            "bg": "#ffffff" if active_button != 'showAllStudentsButton' else "#6FFD9D",
            "fg": "#000000",
            "activebackground": "#ffffff" if active_button != 'showAllStudentsButton' else "#62E48C",
            "activeforeground": "#000000",
            "highlightthickness": 0,
            "relief": tk.FLAT,
            "justify": tk.LEFT,
            "pady": 16
        },
        "initializeSystem": {
            "bg": "#ffffff" if active_button != 'initializeSystem' else "#6FFD9D",
            "fg": "#000000",
            "activebackground": "#ffffff" if active_button != 'initializeSystem' else "#62E48C",
            "activeforeground": "#000000",
            "highlightthickness": 0,
            "relief": tk.FLAT,
            "justify": tk.LEFT,
            "pady": 16
        },

    }

    addStudentButton = tk.Button(
        master=leftButtonsFrame, text="Add student", font=font, command=onAddStudentButtonPress, borderwidth=0, **buttonsConfig['addStudentButton'])
    addStudentButton.pack(fill=tk.X)

    showAllStudentsButton = tk.Button(
        master=leftButtonsFrame, text="Show All students", font=font, command=onShowAllStudentsButtonPress, borderwidth=0, **buttonsConfig['showAllStudentsButton'])
    showAllStudentsButton.pack(fill=tk.X)

    initializeSystem = tk.Button(
        master=leftButtonsFrame, text="Start Attendance", font=font, command=onInitializeSystemButtonPress, borderwidth=0, **buttonsConfig['initializeSystem'])
    initializeSystem.pack(fill=tk.X)

    getAttendanceReportButton = tk.Button(
        master=leftButtonsFrame, text="Get attendance report", font=font, command=getReport, borderwidth=0, bg="#E5FFEE", fg="#000000", activebackground="#ffffff", activeforeground="#000000", highlightthickness=0, relief=tk.FLAT, justify=tk.LEFT, pady=16)
    getAttendanceReportButton.pack(
        fill=tk.X)
    emptyFrame = ctk.CTkFrame(
        master=leftButtonsFrame, bg_color="transparent", fg_color="transparent")
    emptyFrame.pack(fill=tk.Y, expand=True, before=getAttendanceReportButton)

    rightFrame = ctk.CTkFrame(
        master=root_window, bg_color="transparent", fg_color="#ffffff", width=960)
    rightFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    showContent(rightFrame, active_button, root_window)
