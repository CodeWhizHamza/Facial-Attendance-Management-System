import tkinter as tk


def main():
    window = tk.Tk()
    window.title("Start Attendance")
    window.geometry('720x520')

    tk.Label(master=window, text='For Ahmed',
             font='Arial 20 roman normal').pack()

    window.mainloop()
