import tkinter as tk
from tkinter import ttk
import cv2 as cv
import face_recognition
import sqlite3
import csv
import os
from tkinter.messagebox import showwarning
import customtkinter as ctk
from config import *


def main(rightFrame):

    font40 = ctk.CTkFont('Arial', 40)
    font24 = ctk.CTkFont('Arial', 24)

    faceEncodings = tk.Variable()

    def showMessage(text):
        showwarning("Warning", text)

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

        if len(faces) > 1:
            showMessage("Multiple faces detected.")
            return

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

        try:
            studentCmsID = int(studentCmsID)
        except:
            showMessage("Please enter a valid CMS ID (integer)")
            return False

        if len(studentSemester) == 0:
            showMessage("Please enter a valid semester number")
            return False

        try:
            studentSemester = int(studentSemester)
        except:
            showMessage("Please enter a valid semester number (integer)")
            return False

        if not faceEncodings.get():
            showMessage("Please provide an image.")
            return False

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
            showMessage("Student already exists.")
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

    emptyFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", height=120)
    emptyFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=80)
    rightHeaderFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderLabel = tk.Label(
        master=rightHeaderFrame, text="Add Student", font=font40, bg="#ffffff", fg="#333333", justify='left', anchor='w', wraplength=960)
    rightHeaderLabel.pack(fill=tk.X, side=tk.LEFT, padx=80)

    entriesFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=400)
    entriesFrame.pack(side=tk.TOP, fill=tk.X, padx=80, pady=64)

    # Printing name input
    nameLabel = ctk.CTkLabel(master=entriesFrame, text="Name: ", font=font24)
    nameEntry = ctk.CTkEntry(master=entriesFrame, font=font24, width=300)
    nameLabel.grid(column=0, row=0, sticky=tk.W)
    nameEntry.grid(column=1, row=0, padx=24)

    # Printing CMS ID input
    cmsIdLabel = ctk.CTkLabel(
        master=entriesFrame, text="CMS ID: ", font=font24)
    cmsIdEntry = ctk.CTkEntry(master=entriesFrame, font=font24, width=300)
    cmsIdLabel.grid(column=0, row=1, sticky=tk.W)
    cmsIdEntry.grid(column=1, row=1, padx=24, pady=24)

    # Printing the semester input
    semesterLabel = ctk.CTkLabel(master=entriesFrame, text="Semester: ",
                                 font=font24)
    semesterEntry = ctk.CTkEntry(master=entriesFrame, font=font24, width=300)
    semesterLabel.grid(column=0, row=2, sticky=tk.W)
    semesterEntry.grid(column=1, row=2, padx=24)

    # Printing take image button
    takeImageLabel = ctk.CTkLabel(master=entriesFrame, text="Your image: ",
                                  font=font24)
    takeImageButton = tk.Button(master=entriesFrame, text="Take Image",
                                font=font24, command=takeImage, bg="#6FFD9D", fg="#333333", activebackground="#62E48C", activeforeground="#333333", bd=0, highlightthickness=0, relief=tk.FLAT, padx=24, pady=12)
    takeImageLabel.grid(column=0, row=3, sticky=tk.W)
    takeImageButton.grid(column=1, row=3, pady=24, sticky=tk.W, padx=24)

    saveButton = tk.Button(master=rightFrame, text="Save",
                           font=font24, command=saveData, bg="#6FFD9D", fg="#333333", activebackground="#62E48C", activeforeground="#333333", bd=0, highlightthickness=0, relief=tk.FLAT, padx=64, pady=12)
    saveButton.pack(side=tk.LEFT, padx=80, pady=0, anchor=tk.W)
