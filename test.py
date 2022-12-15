import tkinter as tk
import sqlite3

from config import *


root = tk.Tk()

reportFrame = tk.Frame(master=root)
reportFrame.pack()

for index, course in enumerate(list(courses)):
    tk.Label(master=reportFrame, text=f"{course}:", font=("Times New Roman", 24)).grid(
        row=index, column=0,  sticky=tk.E, padx=8)
    tk.Label(master=reportFrame, text=f"{70}%", font=("Times New Roman", 24)).grid(
        row=index, column=1,  sticky=tk.W, padx=8)

root.mainloop()
