from tkinter import ttk
import tkinter as tk
import sqlite3
from config import *

from edit_student_details import editStudent
from delete_student import deleteStudent
from helper import printTable


def main():

    root = tk.Tk()
    root.title("Student details")
    root.geometry('720x480')

    studentDetails = tk.Variable()

    heading = tk.Label(master=root, text="Student Details",
                       font='Arial 24 roman normal')
    heading.pack(pady=18)

    def selectRecord(item):
        item = table.selection()
        studentDetails.set(table.item(item)['values'])

    def editStudentDetails():
        if not studentDetails.get():
            print("No student selected.")
        else:
            editStudent(studentDetails.get()[0], table)

    def deleteStudentDetails():
        if not studentDetails.get():
            print("No student selected.")

        deleteStudent(studentDetails.get()[0], table)

    table = ttk.Treeview(root)

    scrollbar = ttk.Scrollbar(
        master=root, orient='vertical', command=table.yview)
    scrollbar.place(relx=0.835, rely=0.16, relheight=0.475, relwidth=0.020)

    table.configure(yscrollcommand=scrollbar.set)

    table.bind('<ButtonRelease-1>', selectRecord)

    table['columns'] = ('CMS ID', 'Name', 'Semester',
                        'Average attendance')

    table.column("#0", width=0, stretch=tk.NO)
    table.column("CMS ID", anchor=tk.CENTER, width=120)
    table.column("Name", anchor=tk.W, width=120)
    table.column("Semester", anchor=tk.CENTER, width=80)
    table.column("Average attendance", anchor=tk.CENTER, width=160)

    # Adding headings
    table.heading('CMS ID', text="CMS ID")
    table.heading('Name', text="Name")
    table.heading('Semester', text="Semester")
    table.heading('Average attendance', text="Average attendance")

    printTable(table)
    table.pack()

    buttonsFrame = tk.Frame(root)
    buttonsFrame.pack(pady=24)

    editButton = ttk.Button(master=buttonsFrame,
                            text="Edit student", command=editStudentDetails)
    deleteButton = ttk.Button(
        master=buttonsFrame, text="Delete student", command=deleteStudentDetails)
    getReportsButton = ttk.Button(
        master=buttonsFrame, text="Get student report")

    getReportsButton.grid(column=0, row=0)
    editButton.grid(column=1, row=0, padx=8)
    deleteButton.grid(column=2, row=0)

    root.mainloop()


# temporary
if __name__ == "__main__":
    main()
