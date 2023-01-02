import tkinter as tk
import customtkinter as ctk
from PIL import Image

from sideBar import showSidebar

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

window = ctk.CTk()
window.title("AMS")
window.geometry('1280x720')
window.minsize(1280, 720)
window.iconbitmap('resources/logo.ico')
window.config(bg='#ffffff')

font = ctk.CTkFont(family="Arial", size=20)
font16 = ctk.CTkFont(family="Arial", size=16)

showSidebar(window, None)

rightFrame = ctk.CTkFrame(
    master=window, bg_color="transparent", fg_color="#ffffff", width=960)
rightFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


window.mainloop()
