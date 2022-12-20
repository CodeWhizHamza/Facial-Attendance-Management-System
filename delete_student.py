import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
import sqlite3
import os

from config import *
from helper import printTable


def deleteStudent(id, table):

    def deleteStudent(id, table):
        db = sqlite3.connect(databaseName)
        cursor = db.cursor()

        query = f"DELETE FROM {tableName} WHERE cmsId={id};"
        cursor.execute(query)
        db.commit()

        cursor.close()
        db.close()

        os.remove(f"./{directoryName}/{id}.csv")

        for item in table.get_children():
            table.delete(item)
        printTable(table)

    if askyesno(title="Confirm", message="Are you sure to delete this student?"):
        deleteStudent(id, table)
