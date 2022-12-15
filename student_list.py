from tkinter import ttk
import tkinter as tk
import sqlite3
from config import *

from edit_student_details import editStudent
from delete_student import deleteStudent
from helper import printTable


def main():
    # window = tk.Tk()
    # window.title("List of students")
    # window.geometry('720x320')

    # # tree = ttk.Treeview(window, columns=(
    # #     "CMS ID", "Name", "Semester"), show="headings")
    # # tree.column("#1", anchor=tk.CENTER)
    # # tree.heading("#1", text="CMS ID")
    # # tree.column("#2", anchor=tk.CENTER)
    # # tree.heading("#2", text="Name")
    # # tree.column("#3", anchor=tk.CENTER)
    # # tree.heading("#3", text="Semester")
    # # tree.pack()
    # def tree_clicked(_):
    #     print('tree clicked')
    #     ind = tree.selection()
    #     item = tree.item(ind)
    #     print(item['values'])
    # tree = ttk.Treeview(window)
    # tree['columns'] = ("CMS ID", "Name", "Semester")
    # tree.bind('<ButtonRelease-1>', tree_clicked)

    # tree.column("#0", width=0, stretch=tk.NO)
    # tree.column("CMS ID", anchor=tk.CENTER, width=80)
    # tree.column("Name", anchor=tk.W, width=120)
    # tree.column("Semester", anchor=tk.W, width=120)
    # tree.heading("#0", text="", anchor=tk.W)
    # tree.heading("CMS ID", text="CMS ID", anchor=tk.CENTER)
    # tree.heading("Name", text="Name", anchor=tk.W)
    # tree.heading("Semester", text="Semester", anchor=tk.W)
    # data = [[1, 'a', 1], [2, 'b', 1], [3, 'c', 1], [4, 'd', 1]]
    # count = 1
    # for id, name, sem in data:
    #     tree.insert(parent='', index='end', iid=count,
    #                 text='', values=(id, name, sem))
    #     count += 1
    # tree.pack()

    # add_frame = tk.Frame(window)
    # add_frame.pack(pady=20)
    # tk.Label(master=window, text='something',
    #          font='Arial 20 roman normal').pack()

    # window.mainloop()

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

        # empty the table
        # for i in table.get_children():
        #     table.delete(i)
        # print the table again
        # printTable()

    def deleteStudentDetails():
        if not studentDetails.get():
            print("No student selected.")

        deleteStudent(studentDetails.get()[0])

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
