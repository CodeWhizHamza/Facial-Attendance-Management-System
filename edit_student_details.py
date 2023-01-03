"""
Part by: Muhammad Hamza
"""

import tkinter as tk
import customtkinter as ctk
import cv2 as cv
import face_recognition
import sqlite3
import csv
import os

from config import *
from helper import showMessage, truncateWidget
from tkinter.messagebox import showinfo
import student_list


def editStudent(id, rightFrame):
    """This function will edit the student details.

    Args:
        id (number): This is the id of the student whose details are to be edited.
        rightFrame (ctk.CTkFrame): This is the frame in which the details are to be displayed.

    Returns:
        None: This function does not return anything. This is just to stop execution
    """
    studentId = tk.IntVar()
    studentName = tk.StringVar()
    studentSemester = tk.IntVar()
    faceEncodings = tk.Variable()
    font40 = ctk.CTkFont('Arial', 40)
    font24 = ctk.CTkFont('Arial', 24)

    def loadStudentData():
        """This function will load the student data from the database and set it to the global variables."""
        db = sqlite3.connect(databaseName)
        cursor = db.cursor()

        query = f"SELECT * FROM {tableName} WHERE cmsId={id}"
        cursor.execute(query)

        cmsId, name, semester = cursor.fetchall()[0]
        studentId.set(cmsId)
        studentName.set(name)
        studentSemester.set(semester)

        cursor.close()
        db.close()

        # read student encodings
        with open(f"./{directoryName}/{id}.csv") as f:
            reader = csv.reader(f)
            encodings = []

            for code in reader:
                encodings.extend(code)

            encodings = [float(code) for code in encodings]
            faceEncodings.set(encodings)

    loadStudentData()

    def takeImage():
        """This function will take the image of the student. This uses opencv to capture the image."""
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
        encodings = [value for value in encodings]
        faceEncodings.set(encodings)

    def validateUserData():
        """This function will validate the user data.

        Returns:
            bool: This function will return True if the data is valid else it will return False.
        """
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

    def updateData():
        """This function will update the data in the database."""
        isValid = validateUserData()
        if not isValid:
            return
        studentName = nameEntry.get()
        studentCmsID = cmsIdEntry.get()
        studentSemester = semesterEntry.get()

        # Connecting with database
        db = sqlite3.connect(databaseName)
        cursor = db.cursor()

        # Adding student data into the table
        query = f"""UPDATE {tableName}
                    SET cmsId={studentCmsID},
                        name='{studentName}',
                        semester={studentSemester}
                    WHERE cmsId={id};"""
        cursor.execute(query)
        db.commit()

        # Closing connection with database
        cursor.close()
        db.close()
        """
        Creating a csv file where I would store
        face encodings for student
        """

        os.remove(f"./{directoryName}/{id}.csv")
        isDirectoryAlreadyPresent = os.path.exists(directoryName)
        if not isDirectoryAlreadyPresent:
            os.makedirs(directoryName)

        with open(f"{directoryName}/{studentCmsID}.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(faceEncodings.get())

        showinfo("Success", "Student data updated successfully.")
        student_list.main(rightFrame)

    truncateWidget(rightFrame)

    emptyFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", height=120)
    emptyFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=80)
    rightHeaderFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderLabel = tk.Label(
        master=rightHeaderFrame, text="Edit Student Details", font=font40, bg="#ffffff", fg="#333333", justify='left', anchor='w', wraplength=960)
    rightHeaderLabel.pack(fill=tk.X, side=tk.LEFT, padx=80)

    entriesFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=400)
    entriesFrame.pack(side=tk.TOP, fill=tk.X, padx=80, pady=64)

    # Printing name input
    nameLabel = ctk.CTkLabel(master=entriesFrame, text="Name: ", font=font24)
    nameEntry = ctk.CTkEntry(master=entriesFrame, font=font24, width=300)
    nameLabel.grid(column=0, row=0, sticky=tk.W)
    nameEntry.grid(column=1, row=0, padx=24)

    nameEntry.delete(0, tk.END)
    nameEntry.insert(0, studentName.get())

    # Printing CMS ID input
    cmsIdLabel = ctk.CTkLabel(
        master=entriesFrame, text="CMS ID: ", font=font24)
    cmsIdEntry = ctk.CTkEntry(master=entriesFrame, font=font24, width=300)
    cmsIdLabel.grid(column=0, row=1, sticky=tk.W)
    cmsIdEntry.grid(column=1, row=1, padx=24, pady=24)

    cmsIdEntry.delete(0, tk.END)
    cmsIdEntry.insert(0, studentId.get())

    # Printing the semester input
    semesterLabel = ctk.CTkLabel(master=entriesFrame, text="Semester: ",
                                 font=font24)
    semesterEntry = ctk.CTkEntry(master=entriesFrame, font=font24, width=300)
    semesterLabel.grid(column=0, row=2, sticky=tk.W)
    semesterEntry.grid(column=1, row=2, padx=24)

    semesterEntry.delete(0, tk.END)
    semesterEntry.insert(0, studentSemester.get())

    # Printing take image button
    takeImageLabel = ctk.CTkLabel(master=entriesFrame, text="Your image: ",
                                  font=font24)
    takeImageButton = tk.Button(master=entriesFrame, text="Take Image",
                                font=font24, command=takeImage, bg="#6FFD9D", fg="#333333", activebackground="#62E48C", activeforeground="#333333", bd=0, highlightthickness=0, relief=tk.FLAT, padx=24, pady=12)
    takeImageLabel.grid(column=0, row=3, sticky=tk.W)
    takeImageButton.grid(column=1, row=3, pady=24, sticky=tk.W, padx=24)

    saveButton = tk.Button(master=rightFrame, text="Update",
                           font=font24, command=updateData, bg="#6FFD9D", fg="#333333", activebackground="#62E48C", activeforeground="#333333", bd=0, highlightthickness=0, relief=tk.FLAT, padx=64, pady=12)
    saveButton.pack(side=tk.LEFT, padx=80, pady=0, anchor=tk.W)

    # Back button
    backButton = tk.Button(master=rightFrame, text="Back",
                           font=font24, command=lambda: student_list.main(rightFrame), bg="#6FFD9D", fg="#333333", activebackground="#62E48C", activeforeground="#333333", bd=0, highlightthickness=0, relief=tk.FLAT, padx=64, pady=12)
    backButton.place(x=80, y=40)
