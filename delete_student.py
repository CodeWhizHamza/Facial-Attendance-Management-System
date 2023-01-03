from tkinter.messagebox import askyesno
import sqlite3
import os

from config import *
import student_list
from helper import truncateWidget


def deleteStudent(id, table, rightFrame):
    """This function will delete the student.

    Args:
        id (number): This is the id of the student to be deleted.
        table (tkinter.Treeview): This is the table in which the student is to be deleted.
        rightFrame (ctk.CTkFrame): This is the frame in which the student is to be deleted.
    """
    def deleteStudent(id, table):
        """This function will delete the student.

        Args:
            id (number): This is the id of the student to be deleted.
            table (tkinter.Treeview): This is the table in which the student is to be deleted.
        """
        db = sqlite3.connect(databaseName)
        cursor = db.cursor()

        query = f"DELETE FROM {tableName} WHERE cmsId={id};"
        cursor.execute(query)
        db.commit()

        for course in courses:
            query = f"ALTER TABLE {course} DROP COLUMN `{id}`;"
            cursor.execute(query)
            db.commit()

        cursor.close()
        db.close()

        os.remove(f"./{directoryName}/{id}.csv")

        for item in table.get_children():
            table.delete(item)

        truncateWidget(rightFrame)
        student_list.main(rightFrame)

    if askyesno(title="Confirm", message="Are you sure to delete this student?"):
        deleteStudent(id, table)
