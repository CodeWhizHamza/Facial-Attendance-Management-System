"""
Part by: Muhammad Hamza
"""

import customtkinter as ctk

from sideBar import showSidebar

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

# Root window
window = ctk.CTk()
window.title("AMS")
window.geometry('1280x720')
window.minsize(1280, 720)
window.iconbitmap('resources/logo.ico')
window.config(bg='#ffffff')

font = ctk.CTkFont(family="Inter", size=20)
font16 = ctk.CTkFont(family="Inter", size=16)
fontTitle = ctk.CTkFont(family="Inter", size=64)

showSidebar(window, None)

window.mainloop()
