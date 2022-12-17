import tkinter as tk
from tkinter import ttk
import cv2 as cv
import face_recognition
import sqlite3
import csv
import os
import customtkinter as ctk

from config import *

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


def main():
    window = ctk.CTk()
    window.title("Add student")
    window.geometry('720x480')
    window.call('wm', 'iconphoto', window._w,
                tk.PhotoImage(file=r'resources/logo.png'))

    font24 = ctk.CTkFont('Arial', 24)
    font16 = ctk.CTkFont('Arial', 16)
    font14 = ctk.CTkFont('Arial', 14)

    faceEncodings = tk.Variable()

    def showMessage(text):
        messageStr.set(text)
        message.configure(text=messageStr.get())

    def takeImage():
        capture = cv.VideoCapture(0)

        if not capture:
            showMessage("Cannot open web cam.")

        ret, frame = capture.read()

        if not ret:
            showMessage("Cannot get frame from camera")

        faces = face_recognition.face_locations(frame)

        if len(faces) == 0:
            showMessage("No face detected.")
            return
        else:
            showMessage("")

        if len(faces) > 1:
            showMessage("Multiple faces detected.")
            return
        else:
            showMessage("")

        face = faces[0]
        cv.rectangle(frame, (face[3], face[0]),
                     (face[1], face[2]), (255, 255, 255), 1)
        cv.imshow("Image", frame)

        encodings = face_recognition.face_encodings(frame, [face])[0]
        encodingsInString = [str(value) for value in encodings]
        encodingsInString = ",".join(encodingsInString)
        faceEncodings.set(encodingsInString)

    def validateUserData():
        studentName = nameEntry.get()
        studentCmsID = cmsIdEntry.get()
        studentSemester = semesterEntry.get()

        if len(studentName) == 0:
            showMessage("Please enter a valid name")
            return False
        else:
            showMessage("")

        try:
            studentCmsID = int(studentCmsID)
        except:
            showMessage("Please enter a valid CMS ID (integer)")
            return False

        if len(studentSemester) == 0:
            showMessage("Please enter a valid semester number")
            return False
        else:
            showMessage("")

        try:
            studentSemester = int(studentSemester)
        except:
            showMessage("Please enter a valid semester number (integer)")
            return False

        if not faceEncodings.get():
            showMessage("Please provide an image.")
            return False
        else:
            showMessage("")

        return True

    def isIdUnique(cursor, id):
        cursor.execute(f"SELECT * FROM {tableName} WHERE cmsId={id};")
        if len(cursor.fetchall()) == 0:
            return True
        else:
            return False

    def addNewColumnToEachCourseTable(columnName):
        db = sqlite3.connect(databaseName)
        cursor = db.cursor()
        for course in courses:
            query = f"""
                ALTER TABLE {course}
                ADD COLUMN `{columnName}` TEXT;
            """
            cursor.execute(query)
            db.commit()

        cursor.close()
        db.close()

    def createTablesIfNotExists():
        db = sqlite3.connect(databaseName)
        cursor = db.cursor()

        cursor.execute(f"SELECT cmsId FROM {tableName};")
        ids = [f"'{id}' TEXT" for id, in cursor.fetchall()]
        ids = ", ".join(ids)
        for course in courses:
            query = f"CREATE TABLE IF NOT EXISTS {course} (dayTime TEXT PRIMARY KEY, {ids});"
            cursor.execute(query)
            db.commit()

        cursor.close()
        db.close()

    def saveData():
        isValid = validateUserData()
        if not isValid:
            return
        studentName = nameEntry.get()
        studentCmsID = cmsIdEntry.get()
        studentSemester = semesterEntry.get()

        # Connecting with database
        db = sqlite3.connect(databaseName)
        cursor = db.cursor()

        """
        Creating a table with schema if it doesn't exists
        CMS ID, Name, Semester
        """
        query = f"""
        CREATE TABLE IF NOT EXISTS {tableName}(
            cmsId INTEGER NOT NULL PRIMARY KEY UNIQUE,
            name TEXT,
            semester INTEGER
        ); """
        cursor.execute(query)
        db.commit()

        # Check if the CMS ID is unique
        if not isIdUnique(cursor, studentCmsID):
            showMessage("This Id already exists.")
            cursor.close()
            db.close()
            return

        # Adding student data into the table
        query = f"""
            INSERT INTO {tableName}
            VALUES ({studentCmsID}, '{studentName}', {studentSemester});
        """
        cursor.execute(query)
        db.commit()

        cursor.close()
        db.close()

        """
        Creating a csv file where I would store
        face encodings for student
        """
        isDirectoryAlreadyPresent = os.path.exists(directoryName)
        if not isDirectoryAlreadyPresent:
            os.makedirs(directoryName)

        with open(f"{directoryName}/{studentCmsID}.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(faceEncodings.get().split(','))

        window.destroy()
        createTablesIfNotExists()
        addNewColumnToEachCourseTable(studentCmsID)

    titleFrame = ctk.CTkFrame(master=window)
    titleFrame.pack(pady=24)
    title = ctk.CTkLabel(
        master=titleFrame, text="Add students", font=font24)
    title.pack(pady=16, padx=48)

    messageStr = tk.StringVar()
    message = ctk.CTkLabel(
        window, font=font14, text=None, text_color="#ff0550")
    message.pack()

    entriesFrame = ctk.CTkFrame(window)
    entriesFrame.pack()

    # Printing name input
    nameLabel = ctk.CTkLabel(entriesFrame, text="Name: ", font=font16)
    nameEntry = ctk.CTkEntry(entriesFrame, font=font16, width=220)
    nameLabel.grid(column=0, row=0, padx=16, sticky=tk.W)
    nameEntry.grid(column=1, row=0, pady=12, padx=24)

    # Printing CMS ID input
    cmsIdLabel = ctk.CTkLabel(entriesFrame, text="CMS ID: ", font=font16)
    cmsIdEntry = ctk.CTkEntry(entriesFrame, font=font16, width=220)
    cmsIdLabel.grid(column=0, row=1, padx=16, sticky=tk.W)
    cmsIdEntry.grid(column=1, row=1, padx=24)

    # Printing the semester input
    semesterLabel = ctk.CTkLabel(entriesFrame, text="Semester: ",
                                 font=font16)
    semesterEntry = ctk.CTkEntry(entriesFrame, font=font16, width=220)
    semesterLabel.grid(column=0, row=2, padx=16, sticky=tk.W)
    semesterEntry.grid(column=1, row=2, pady=12, padx=24)

    # Printing take image button
    takeImageButton = ctk.CTkButton(
        master=entriesFrame, text="Take image", command=takeImage)
    takeImageButton.grid(column=1, row=3, pady=10, padx=24, sticky=tk.W)

    # Printing Buttons
    cancelButton = ctk.CTkButton(
        entriesFrame, text="Cancel", command=lambda: window.destroy())
    saveButton = ctk.CTkButton(entriesFrame, text="Save",
                               command=saveData)

    saveButton.grid(column=1, row=4, sticky=tk.W, padx=24)
    cancelButton.grid(column=1, row=5, sticky=tk.W, pady=8, padx=24)

    window.mainloop()


if __name__ == "__main__":
    main()
