"""
Part by: Maheen Ahmed
"""

from tkinter import ttk
import tkinter as tk
import customtkinter as ctk
from config import *
import os

from edit_student_details import editStudent
from delete_student import deleteStudent
from student_report import studentReport
from helper import printTable, truncateWidget


def main(rightFrame):
    """This function will display the student list.

    Args:
        rightFrame (ctk.CTkFrame): This is the right frame.
    """
    font40 = ctk.CTkFont('Arial', 40)
    font24 = ctk.CTkFont('Arial', 24)
    studentDetails = tk.Variable()

    truncateWidget(rightFrame)

    # the empty space above any other widget
    emptyFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", height=120)
    emptyFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=80)
    rightHeaderFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderLabel = tk.Label(
        master=rightHeaderFrame, text="Student details", font=font40, bg="#ffffff", fg="#333333", justify='left', anchor='w', wraplength=960)
    rightHeaderLabel.pack(fill=tk.X, side=tk.LEFT, padx=80)

    def selectRecord(item):
        """This function will select the record.

        Args:
            item (Treeview.Item): This is the item to be selected.
        """
        item = table.selection()
        studentDetails.set(table.item(item)['values'])

    def studentSelected():
        """This function will check if a student is selected.

        Returns:
            bool: This is the result of the check.
        """
        if not studentDetails.get():
            tk.messagebox.showinfo("Info", "No student selected.")
            return False
        else:
            return True

    def editStudentDetails():
        """This function will edit the student details."""
        if studentSelected():
            studentId = studentDetails.get()[0]
            editStudent(studentId, rightFrame)

    def deleteStudentDetails():
        """This function will delete the student details."""
        if studentSelected():
            studentId = studentDetails.get()[0]
            deleteStudent(studentId, table, rightFrame)

    def getStudentReport():
        """This function will get the student report."""
        if studentSelected():
            studentId = studentDetails.get()[0]
            studentReport(studentId, rightFrame)

    # if no students are found, show a message
    if not os.path.exists('./known_encodings'):
        labelFrame = ctk.CTkFrame(
            master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=80)
        labelFrame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(master=labelFrame, text="No students found. Please add students first", bg='#ffffff', fg='#333333',
                 wraplength=800, justify='left', anchor='w', font=font24).pack(side=tk.TOP, fill=tk.X, padx=80, pady=32)
        return

    # if no students are found, show a message
    if len(os.listdir('./known_encodings')) == 0:
        labelFrame = ctk.CTkFrame(
            master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=80)
        labelFrame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(master=labelFrame, text="No students found. Please add students first", bg='#ffffff', fg='#333333',
                 wraplength=800, justify='left', anchor='w', font=font24).pack(side=tk.TOP, fill=tk.X, padx=80, pady=32)
        return

    tableFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=640)
    tableFrame.pack(side=tk.TOP, fill=tk.X, padx=80, pady=64, anchor=tk.W)

    # styles for treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=font24)
    style.configure("Treeview", font=font24, rowheight=32, width=900)
    table = ttk.Treeview(tableFrame, selectmode='browse', show='headings')
    scrollbar = ttk.Scrollbar(
        master=rightFrame, orient='vertical', command=table.yview)
    scrollbar.place(relx=0.98, rely=0.12, relheight=0.470, relwidth=0.020)

    table.configure(yscrollcommand=scrollbar.set)
    table.bind('<<TreeviewSelect>>', selectRecord)

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
    table.pack(side=tk.TOP, fill=tk.X)

    editButton = tk.Button(master=rightFrame, text="Edit student",
                           font=font24, command=editStudentDetails, bg="#6FFD9D", fg="#333333", activebackground="#62E48C", activeforeground="#333333", bd=0, highlightthickness=0, relief=tk.FLAT, padx=32, pady=12)
    deleteButton = tk.Button(master=rightFrame, text="Delete student",
                             font=font24, command=deleteStudentDetails, bg="#FF6F6F", fg="#333333", activebackground="#E46262", activeforeground="#333333", bd=0, highlightthickness=0, relief=tk.FLAT, padx=32, pady=12)
    getReportsButton = tk.Button(master=rightFrame, text="Get student report",
                                 font=font24, command=getStudentReport, bg="#6F6FFF", fg="#ffffff", activebackground="#6262E4", activeforeground="#ffffff", bd=0, highlightthickness=0, relief=tk.FLAT, padx=32, pady=12)
    tk.Label(master=rightFrame, text="", bg="#ffffff", fg="#ffffff").pack(
        side=tk.LEFT, padx=40)
    editButton.pack(side=tk.LEFT, pady=16)
    deleteButton.pack(side=tk.LEFT, padx=32, pady=16)
    getReportsButton.pack(side=tk.LEFT, pady=16)
