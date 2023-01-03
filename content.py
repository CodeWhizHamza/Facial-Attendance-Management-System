import tkinter as tk
import customtkinter as ctk
from PIL import Image

import add_student
import student_list
import verify_admin
from helper import truncateWidget


def showContent(rightFrame, active_button=None, root_window=None):
    """This function will show the content.

    Args:
        rightFrame (ctk.CTkFrame): This is the right frame.
        active_button (string, optional): This is the active button. Defaults to None.
        root_window (tk.Tk, optional): This is the root window. Defaults to None.
    """
    fontTitle = ctk.CTkFont(family="Inter", size=64)

    if active_button == 'addStudentButton':
        add_student.main(rightFrame, root_window)
    elif active_button == 'showAllStudentsButton':
        student_list.main(rightFrame)
    elif active_button == 'initializeSystem':
        verify_admin.isAdmin(rightFrame, message="", root_window=root_window)

    if active_button is not None:
        return

    truncateWidget(rightFrame)
    emptyFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", height=120)
    emptyFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=80)
    rightHeaderFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderLabel = tk.Label(
        master=rightHeaderFrame, text="Welcome to attendance management system.", font=fontTitle, bg="#ffffff", fg="#333333", justify='left', anchor='w', wraplength=960)
    rightHeaderLabel.pack(fill=tk.X, side=tk.LEFT, padx=80)

    # add home-image in right frame
    rightImageFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=640)
    rightImageFrame.pack(side=tk.TOP, fill=tk.X)

    rightImage = ctk.CTkLabel(
        rightImageFrame, image=ctk.CTkImage(light_image=Image.open('resources/home-image.png'), dark_image=Image.open('resources/home-image.png'), size=(500, 373)), text="")
    rightImage.pack(side=tk.LEFT, padx=0)
