import tkinter as tk


def main():
    window = tk.Tk()
    window.title("List of students")
    window.geometry('720x320')

    tk.Label(master=window, text='something',
             font='Arial 20 roman normal').pack()

    window.mainloop()
