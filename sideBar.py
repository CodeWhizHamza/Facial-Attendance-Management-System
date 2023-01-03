import tkinter as tk
import customtkinter as ctk
from PIL import Image


from getTotalAttendanceReport import getReport
from content import showContent
from helper import truncateWidget


def showSidebar(root_window, active_button=None):
    """This function will show the sidebar.

    Args:
        root_window (tk.Tk): This is the root window.
        active_button (string, optional): This is the active button. Defaults to None.
    """
    font = ctk.CTkFont(family="Arial", size=20)
    root_window.protocol("WM_DELETE_WINDOW", lambda: root_window.destroy())
    truncateWidget(root_window)

    def onAddStudentButtonPress():
        """This function will show the add student form."""
        active_button = 'addStudentButton'
        showSidebar(root_window, active_button)

    def onShowAllStudentsButtonPress():
        """This function will show the list of all students."""
        active_button = 'showAllStudentsButton'
        showSidebar(root_window, active_button)

    def onInitializeSystemButtonPress():
        """This function will show the initialize system form."""
        active_button = 'initializeSystem'
        showSidebar(root_window, active_button)

    # the sidebar frame
    leftFrame = ctk.CTkFrame(master=root_window, bg_color="#f5f5f5", width=320)
    leftFrame.pack(side=tk.LEFT, fill=tk.Y)

    # display the logo
    logoFrame = ctk.CTkFrame(
        master=leftFrame, bg_color="transparent", fg_color="transparent")
    logoFrame.pack(padx=24, pady=24, fill=tk.X)

    logoImage = ctk.CTkLabel(
        logoFrame, image=ctk.CTkImage(light_image=Image.open('resources/header.png'), dark_image=Image.open('resources/header.png'), size=(277, 77)), text="")
    logoImage.grid(row=0, column=0, sticky=tk.W)

    # sidebar buttons
    leftButtonsFrame = ctk.CTkFrame(
        master=leftFrame, bg_color="transparent", fg_color="transparent")
    leftButtonsFrame.pack(pady=16, fill=tk.BOTH, expand=True)

    # sidebar buttons configuration
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

    # Printing all the buttons
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
