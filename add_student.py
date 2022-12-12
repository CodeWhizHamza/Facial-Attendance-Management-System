import tkinter as tk


def main():
    window = tk.Tk()
    window.title("Add student")
    window.geometry('600x400')

    title = tk.Label(
        master=window, text="Add students", fg='#333', font='Arial 18 roman bold')
    title.pack(pady=18)

    name = tk.Entry(master=window)
    name.pack()

    window.mainloop()
