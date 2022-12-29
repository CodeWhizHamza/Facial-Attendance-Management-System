from tkinter import ttk
import tkinter as tk
import customtkinter as ctk
from config import *

from edit_student_details import editStudent
from delete_student import deleteStudent
from student_report import studentReport
from helper import printTable


def main():
    window = ctk.CTkToplevel()
    window.title("Student details")
    window.geometry('720x480')
    window.iconbitmap('resources/logo.ico')
    window.resizable(width=False, height=False)
    window.focus()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    font24 = ctk.CTkFont('Arial', size=24)

    studentDetails = tk.Variable()

    heading = ctk.CTkLabel(master=window, text="Student Details",
                           font=font24)
    heading.pack(pady=18)

    def selectRecord(item):
        item = table.selection()
        studentDetails.set(table.item(item)['values'])

    def studentSelected():
        if not studentDetails.get():
            tk.messagebox.showinfo("Info", "No student selected.")
            return False
        else:
            return True

    def editStudentDetails():
        if studentSelected():
            studentId = studentDetails.get()[0]
            editStudent(studentId, table)

    def deleteStudentDetails():
        if studentSelected():
            studentId = studentDetails.get()[0]
            deleteStudent(studentId, table)

    def getStudentReport():
        if studentSelected():
            studentId = studentDetails.get()[0]
            studentReport(studentId)

    tableFrame = ctk.CTkFrame(window)
    tableFrame.pack(padx=80, fill=tk.X)

    table = ttk.Treeview(tableFrame, selectmode='extended')
    scrollbar = ttk.Scrollbar(
        master=window, orient='vertical', command=table.yview)
    scrollbar.place(relx=0.98, rely=0.12, relheight=0.470, relwidth=0.020)

    table.configure(yscrollcommand=scrollbar.set)
    table.bind('<ButtonRelease-1>', selectRecord)

    table['columns'] = ('CMS ID', 'Name', 'Semester',
                        'Average attendance')

    table.column("#0", width=0, stretch=tk.NO)
    table.column("CMS ID", anchor=tk.CENTER, width=120)
    table.column("Name", anchor=tk.W, width=300)
    table.column("Semester", anchor=tk.CENTER, width=80)
    table.column("Average attendance", anchor=tk.CENTER, width=160)

    # Adding headings
    table.heading('CMS ID', text="CMS ID")
    table.heading('Name', text="Name")
    table.heading('Semester', text="Semester")
    table.heading('Average attendance', text="Average attendance")

    printTable(table)
    table.pack(pady=20)

    buttonsFrame = ctk.CTkFrame(
        window, bg_color='transparent', fg_color='transparent')
    buttonsFrame.pack(pady=24)

    editButton = ctk.CTkButton(master=buttonsFrame,
                               text="Edit student", command=editStudentDetails)
    deleteButton = ctk.CTkButton(
        master=buttonsFrame, text="Delete student", command=deleteStudentDetails)
    getReportsButton = ctk.CTkButton(
        master=buttonsFrame, text="Get student report", command=getStudentReport)

    getReportsButton.grid(column=0, row=0)
    editButton.grid(column=1, row=0, padx=8)
    deleteButton.grid(column=2, row=0)

    window.mainloop()


if __name__ == "__main__":
    main()
