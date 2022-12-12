import tkinter as tk
from tkinter import ttk


def main():
    window = tk.Tk()
    window.title("Add student")
    window.geometry('600x400')

    def showMessage(text):
        messageStr.set(text)
        message.config(text=messageStr.get())

    def saveData():
        studentName = nameEntry.get()
        studentCmsID = cmsIdEntry.get()
        studentSemester = semesterEntry.get()

        if len(studentName) == 0:
            showMessage("Please enter a valid name")
            return
        else:
            showMessage("")

        try:
            studentCmsID = int(studentCmsID)
        except:
            showMessage("Please enter a valid CMS ID (integer)")
            return

        if len(studentSemester) == 0:
            showMessage("Please enter a valid semester number")
            return
        else:
            showMessage("")

        try:
            studentSemester = int(studentSemester)
        except:
            showMessage("Please enter a valid semester number (integer)")
            return

        print(studentName, studentCmsID, studentSemester)
        window.destroy()

    title = ttk.Label(
        master=window, text="Add students", foreground='#333', font='Arial 18 roman bold')
    title.pack(pady=18)

    messageStr = tk.StringVar()
    message = ttk.Label(
        window, font="Arial 14 roman normal", foreground="#ff0220")
    message.pack()

    entriesFrame = ttk.Frame(window)
    entriesFrame.pack()

    # Printing name input
    nameLabel = ttk.Label(entriesFrame, text="Name: ",
                          foreground='#333', font='Arial 16')
    nameEntry = ttk.Entry(entriesFrame, font="Arial 16 roman normal")
    nameLabel.grid(column=0, row=0)
    nameEntry.grid(column=1, row=0, pady=5)

    # Printing CMS ID input
    cmsIdLabel = ttk.Label(entriesFrame, text="CMS ID: ",
                           foreground='#333', font='Arial 16')
    cmsIdEntry = ttk.Entry(entriesFrame, font="Arial 16 roman normal")
    cmsIdLabel.grid(column=0, row=1)
    cmsIdEntry.grid(column=1, row=1, pady=5)

    # Printing the semester input
    semesterLabel = ttk.Label(entriesFrame, text="Semester: ",
                              foreground='#333', font='Arial 16')
    semesterEntry = ttk.Entry(entriesFrame, font="Arial 16 roman normal")
    semesterLabel.grid(column=0, row=2)
    semesterEntry.grid(column=1, row=2, pady=5)

    # Printing Buttons
    buttonsFrame = ttk.Frame(window)
    buttonsFrame.pack()

    s = ttk.Style()
    s.configure("my.TButton", font="Helvetica 16 roman normal")

    cancelButton = ttk.Button(
        buttonsFrame, text="Cancel", style='my.TButton', command=lambda: window.destroy())
    saveButton = ttk.Button(buttonsFrame, text="Save",
                            style='my.TButton', command=saveData)

    saveButton.grid(column=0, row=0, columnspan=4)
    cancelButton.grid(column=0, row=1, columnspan=4)

    window.mainloop()


main()
