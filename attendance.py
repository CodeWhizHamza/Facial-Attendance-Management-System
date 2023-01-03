import tkinter as tk
import customtkinter as ctk
import cv2 as cv
import face_recognition
from datetime import datetime
import calendar
import threading as th
import json
from PIL import Image, ImageTk
from tkinter import simpledialog
from tkinter import messagebox
import os

from config import *
from helper import *
import sideBar

# global variables
isTimerStarted = False
isEndButtonClicked = False
SECONDS_IN_MINUTE = 60
cmsIDList = []


def showMessage(rightFrame, message, font24, root_window):
    """This function will show the message in the right frame.

    Args:
        rightFrame (ctk.CTkFrame): This is the frame in which the message is to be shown.
        message (string): This is the message to be shown.
        font24 (ctk.CTkFont): This is the font to be used for the message.
        root_window (tk.Tk): This is the root window of the application.
    """
    labelFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=80)
    labelFrame.pack(side=tk.TOP, fill=tk.X)
    tk.Label(master=labelFrame, text=message, bg='#ffffff', fg='#333333',
             wraplength=800, justify='left', anchor='w', font=font24).pack(side=tk.TOP, fill=tk.X, padx=80, pady=32)

    backButton = tk.Button(master=labelFrame, text="Go back",
                           font=font24, command=lambda: sideBar.showSidebar(root_window, None), bg="#6FFD9D", fg="#333333", activebackground="#62E48C", activeforeground="#333333", bd=0, highlightthickness=0, relief=tk.FLAT, padx=64, pady=12)
    backButton.pack(side=tk.LEFT, padx=80)


def main(rightFrame, root_window=None):
    """This function will show the attendance screen.

    Args:
        rightFrame (ctk.CTkFrame): This is the frame in which the attendance screen is to be shown.
        root_window (tk.Tk, optional): This is the root window of the application. Defaults to None.
    """
    font40 = ctk.CTkFont('Inter', 40)
    font24 = ctk.CTkFont('Inter', 24)
    global attendanceShouldRun, cmsIDList
    attendanceShouldRun = False
    cmsIDList = []

    currentDate = datetime.now()
    today = calendar.day_name[currentDate.weekday()]

    # make the right frame empty
    # print the header on screen for this screen
    truncateWidget(rightFrame)
    emptyFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", height=120)
    emptyFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=80)
    rightHeaderFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderLabel = tk.Label(
        master=rightHeaderFrame, text="Attendance", font=font40, bg="#ffffff", fg="#333333", justify='left', anchor='w', wraplength=960)
    rightHeaderLabel.pack(fill=tk.X, side=tk.LEFT, padx=80)

    try:
        file = open('attendanceVariables.json', 'r')
        todayClassesRecord = json.load(file)
        file.close()
    except FileNotFoundError:
        todayClassesRecord = getDefaultAttendanceRecord(today)

    # if it's a weekend
    if today == "Saturday" or today == "Sunday":
        showMessage(
            rightFrame, "It's a weekend. Go and enjoy your Weekend :)", font24, root_window)
        return

    # if it's outside class hours
    if 900 > int(currentDate.strftime("%H%M")) or int(currentDate.strftime("%H%M")) > 1700:
        showMessage(
            rightFrame, "Attendance can only be marked between 9:00 AM to 5:00 PM.", font24, root_window)
        return

    time = datetime.now()
    currentClassTime = time.strftime("%H00")
    currentTimeTable = timeTable.loc[today]

    # if there is no class going on right now
    if currentTimeTable is not None and currentTimeTable[currentClassTime] is None:
        showMessage(rightFrame, "No class is going on right now.",
                    font24, root_window)
        return

    # if no student data is found
    if not os.path.exists('./known_encodings'):
        showMessage(
            rightFrame, "No students data found. Please add students first.", font24, root_window)
        return
    if len(os.listdir('./known_encodings')) == 0:
        showMessage(
            rightFrame, "No students data found. Please add students first.", font24, root_window)
        return

    def endAttendance(overcomeCondition) -> None:
        """This function will end the attendance.

        Args:
            overcomeCondition (bool): this is condition for overcoming password authentication.
        """
        global cmsIDList
        dayTime = currentDate.strftime("%d-%m-%Y-%H00")
        if isTimerStarted:
            markAttendance(
                cmsIDList, currentTimeTable[currentDate.strftime("%H00")], dayTime)

        attendanceTimerThread.cancel()
        if overcomeCondition:
            root_window.destroy()
        else:
            sideBar.showSidebar(root_window)

    def updateFrame(frame, frameContainer):
        """This function will update the frame.

        Args:
            frame (frame): This is the frame to be updated.
            frameContainer (tk.Canvas): This is the canvas on which the frame is to be shown.
        """
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(master=frameContainer, image=img)
        frameContainer.create_image(360, 240, image=photo)
        frameContainer.image = photo

    def printTextOnFrame(frame, text):
        """This function will print the text on the frame.

        Args:
            frame (frame): This is the frame on which the text is to be printed.
            text (str): This is the text to be printed.
        """
        if not len(frame):
            return

        cv.putText(frame, text,
                   (50, 50),  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv.LINE_AA)
        updateFrame(frame, cameraFeedContainer)

    def getCMSIdFor(encoding):
        """This function will return the CMS ID for the encoding.

        Args:
            encoding (list): This is the encoding for which the CMS ID is to be found.

        Returns:
            str: This is the CMS ID for the encoding.
        """
        matches = face_recognition.compare_faces(
            knownEncodings.tolist(), encoding, tolerance=0.44)
        if True not in matches:
            return None

        indexOfMatched = matches.index(True)
        return knownEncodings.index[indexOfMatched]

    def displayMarkerOnFace(frame, face, cmsId):
        """This function will display the marker on the face.

        Args:
            frame (frame): This is the frame on which the marker is to be displayed.
            face (list): This is the face on which the marker is to be displayed.
            cmsId (str): This is the CMS ID of the student.
        """
        top, right, bottom, left = [coord * 4 for coord in face]
        font = cv.FONT_HERSHEY_DUPLEX
        text = "Unknown" if cmsId is None else cmsId
        cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv.rectangle(frame, (left, bottom-35),
                     (right, bottom), (0, 255, 0), cv.FILLED)
        cv.putText(frame, text, (left + 6,
                                 bottom - 6), font, 1.0, (255, 255, 255), 1)

    def addStateToJSON(file, data):
        """This function will add the state to the JSON file.

        Args:
            file (str): This is the file to which the state is to be added.
            data (dict): This is the data to be added.
        """
        with open(file, 'w') as f:
            json.dump(data, f)

    def closeWindow(overcomeCondition=False):
        """This function will close the window.

        Args:
            overcomeCondition (bool, optional): This is the condition for overcoming password authentication. Defaults to False.
        """
        global isEndButtonClicked
        isEndButtonClicked = True
        if not overcomeCondition:
            if simpledialog.askstring("Input", "Enter the password") != password:
                messagebox.showerror("Error", "Wrong password")
                return
        addStateToJSON('attendanceVariables.json', todayClassesRecord)
        capture.release()
        endAttendance(overcomeCondition)

    attendanceDuration = 15 * SECONDS_IN_MINUTE
    attendanceTimerThread = th.Timer(attendanceDuration, endAttendance)

    if todayClassesRecord["day"] != today:
        todayClassesRecord = getDefaultAttendanceRecord(today)

    if todayClassesRecord[currentClassTime] != 0:
        showMessage(
            rightFrame, "Attendance has already been marked for this class.", font24, root_window)
        return

    currentClassName = None
    if currentTimeTable is not None:
        currentClassName = currentTimeTable[currentClassTime] if currentTimeTable[currentClassTime] else "No class"

    rightHeaderLabel.configure(text=f"Attendance for {currentClassName}")

    capture = cv.VideoCapture(0)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 720)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    knownEncodings = getKnownEncodings()

    def mainLoop() -> None:
        """This is the main loop of the attendance system.

        Returns:
            None: This function does not return anything.
        """
        global isTimerStarted
        global cmsIDList
        cmsIDList = []
        if not isTimerStarted:
            attendanceTimerThread.start()
        todayClassesRecord[currentClassTime] = 1
        isTimerStarted = True
        frame = getFrameInRGB(capture)
        if not len(frame):
            return

        smallFrame = cv.resize(frame, (0, 0), fy=0.25, fx=0.25)
        faces = face_recognition.face_locations(smallFrame)

        # if there or more than one person in the frame
        if len(faces) != 1:
            printTextOnFrame(
                frame, "One person is allowed in frame.")
            updateFrame(frame, cameraFeedContainer)
            return

        currentFace = faces[0]
        face_encoding = face_recognition.face_encodings(
            smallFrame, faces)[0]
        cmsId = getCMSIdFor(face_encoding)
        displayMarkerOnFace(frame, currentFace, cmsId)
        if cmsId and cmsId not in cmsIDList:
            cmsIDList.append(cmsId)

        updateFrame(frame, cameraFeedContainer)

    cameraFeedFrame = tk.Frame(rightFrame, width=720, height=440)
    cameraFeedFrame.pack(side=tk.TOP, padx=80, anchor=tk.W,  pady=24)
    cameraFeedContainer = tk.Canvas(cameraFeedFrame, width=720, height=440)
    cameraFeedContainer.pack(side=tk.LEFT)

    endButton = tk.Button(master=rightFrame, text="End attendance",
                          font=font24, command=closeWindow, bg="#6FFD9D", fg="#333333", activebackground="#62E48C", activeforeground="#333333", bd=0, highlightthickness=0, relief=tk.FLAT, padx=64, pady=12)
    endButton.pack(side=tk.TOP, padx=80, anchor=tk.W)

    def startCamera():
        """This function will start the camera."""
        global isEndButtonClicked
        mainLoop()
        if not isEndButtonClicked:
            root_window.after(1, startCamera)

    startCamera()
    root_window.protocol("WM_DELETE_WINDOW", lambda: closeWindow(True))
