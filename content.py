import tkinter as tk
import customtkinter as ctk
from PIL import Image

import add_student
import attendance
import student_list


def showContent(root_window, active_button):
    fontTitle = ctk.CTkFont(family="Inter", size=64)
    rightFrame = ctk.CTkFrame(
        master=root_window, bg_color="transparent", fg_color="#ffffff", width=960)
    rightFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    if active_button == 'addStudentButton':
        add_student.main(rightFrame)
    elif active_button == 'showAllStudentsButton':
        student_list.main(rightFrame)
    elif active_button == 'initializeSystem':
        attendance.main(rightFrame)

    if active_button is not None:
        return

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
