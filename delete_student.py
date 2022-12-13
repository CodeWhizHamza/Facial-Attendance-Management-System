import tkinter as tk
from tkinter import ttk
import sqlite3
import os

from config import *


def deleteStudent(id):
    window = tk.Tk()
    window.title("Are you sure?")
    window.geometry('240x160')

    # when user clicks cancel button
    def cancel():
        window.destroy()

    def deleteStudent(id):
        db = sqlite3.connect(databaseName)
        cursor = db.cursor()

        query = f"DELETE FROM {tableName} WHERE cmsId={id};"
        cursor.execute(query)
        db.commit()

        cursor.close()
        db.close()

        os.remove(f"./{directoryName}/{id}.csv")

        window.destroy()

    messageLabel = ttk.Label(
        window, text="Are you sure, and want to delete this student?", font="Arial 16", wraplength=230)
    messageLabel.pack(pady=24)

    buttonsFrame = ttk.Frame(master=window)
    buttonsFrame.pack()

    yesButton = ttk.Button(master=buttonsFrame,
                           text="Yes", command=lambda: deleteStudent(id))
    noButton = ttk.Button(master=buttonsFrame, text="Cancel", command=cancel)

    yesButton.grid(row=0, column=0, sticky=tk.E)
    noButton.grid(row=0, column=1, sticky=tk.E)

    window.mainloop()


if __name__ == "__main__":
    deleteStudent(407252)
