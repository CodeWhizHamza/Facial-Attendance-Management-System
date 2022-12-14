import tkinter as tk
from tkinter import ttk
import cv2 as cv
import face_recognition
import sqlite3
import csv
import os

from config import *


def editStudent(id):
    window = tk.Tk()
    window.title("Edit student")
    window.geometry('600x400')

    studentId = tk.IntVar()
    studentName = tk.StringVar()
    studentSemester = tk.IntVar()
    faceEncodings = tk.Variable()

    def loadStudentData():
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

        with open(f"./{directoryName}/{id}.csv") as f:
            reader = csv.reader(f)
            encodings = []

            for code in reader:
                encodings.extend(code)

            encodings = [float(code) for code in encodings]
            faceEncodings.set(encodings)

    loadStudentData()

    def showMessage(text):
        messageStr.set(text)
        message.config(text=messageStr.get())

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
        encodings = [value for value in encodings]
        # encodingsInString = ",".join(encodingsInString)
        faceEncodings.set(encodings)

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

        window.destroy()

    title = ttk.Label(
        master=window, text="Update student details", foreground='#333', font='Arial 18 roman bold')
    title.pack(pady=18)

    messageStr = tk.StringVar()
    message = ttk.Label(
        window, font="Arial 14 roman normal", foreground="#ff0220")
    message.pack()

    entriesFrame = ttk.Frame(window)
    entriesFrame.pack()

    # Printing name input
    nameLabel = ttk.Label(entriesFrame, text="Name: ",
                          foreground='#333', font='Arial 16')
    nameEntry = ttk.Entry(
        entriesFrame, font="Arial 16 roman normal", textvariable=studentName)
    nameLabel.grid(column=0, row=0)
    nameEntry.grid(column=1, row=0, pady=5)

    # Printing CMS ID input
    cmsIdLabel = ttk.Label(entriesFrame, text="CMS ID: ",
                           foreground='#333', font='Arial 16')
    cmsIdEntry = ttk.Entry(
        entriesFrame, font="Arial 16 roman normal", textvariable=studentId)
    cmsIdLabel.grid(column=0, row=1)
    cmsIdEntry.grid(column=1, row=1, pady=5)

    # Printing the semester input
    semesterLabel = ttk.Label(entriesFrame, text="Semester: ",
                              foreground='#333', font='Arial 16')
    semesterEntry = ttk.Entry(
        entriesFrame, font="Arial 16 roman normal", textvariable=studentSemester)
    semesterLabel.grid(column=0, row=2)
    semesterEntry.grid(column=1, row=2, pady=5)

    s = ttk.Style()
    s.configure("my.TButton", font="Helvetica 16 roman normal")

    # Printing take image button
    takeImageButton = ttk.Button(
        master=entriesFrame, text="Take image", style="my.TButton", command=takeImage)
    takeImageButton.grid(column=1, row=3, sticky=tk.W, pady=10)

    # Printing Buttons
    cancelButton = ttk.Button(
        entriesFrame, text="Cancel", style='my.TButton', command=lambda: window.destroy())
    saveButton = ttk.Button(entriesFrame, text="Save",
                            style='my.TButton', command=saveData)

    saveButton.grid(column=1, row=4, sticky=tk.W)
    cancelButton.grid(column=1, row=5, sticky=tk.W)

    window.mainloop()


if __name__ == "__main__":
    editStudent(4221)
