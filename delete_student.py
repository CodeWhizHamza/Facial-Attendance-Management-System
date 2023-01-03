import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
import sqlite3
import os

from config import *
import student_list
from helper import truncateWidget


def deleteStudent(id, table, rightFrame):

    def deleteStudent(id, table):
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
