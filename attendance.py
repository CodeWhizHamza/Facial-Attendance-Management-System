import tkinter as tk
import customtkinter as ctk
import cv2 as cv
import face_recognition
from tkinter import ttk
from datetime import datetime
import calendar
import threading as th
import json
from PIL import Image, ImageTk

from config import *
from helper import *

# TODO: if you can declare them inside the main loop of tkinter, remove all the global things.
isTimerStarted = False
attendanceShouldRun = False
SECONDS_IN_MINUTE = 60
cmsIDList = []


def main():
    window = tk.Tk()
    window.title("Start Attendance")
    window.geometry('720x520')
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    cameraShouldStart = True
    global attendanceShouldRun, cmsIDList
    attendanceShouldRun = False
    cmsIDList = []

    currentDate = datetime.now()
    today = calendar.day_name[currentDate.weekday()]

    try:
        file = open('attendanceVariables.json', 'r')
        todayClassesRecord = json.load(file)
        file.close()
    except FileNotFoundError:
        todayClassesRecord = getDefaultAttendanceRecord(today)

    if today == "Saturday" or today == "Sunday":
        exitLabel = tk.Label(
            window, text="It's a weekend, GO and enjoy your Weekend\n:)", font="Arial 24")
        exitLabel.pack()
        exitButton = ctk.CTkButton(
            window, text="Close Window", command=lambda: window.destroy())
        exitButton.pack()
        cameraShouldStart = False

    elif 900 > int(currentDate.strftime("%H%M")) or int(currentDate.strftime("%H%M")) > 1700:
        exitLabel = tk.Label(
            window, text="You Tried to initialize system out of class Hours.\n Please try again later -_-", font="Arial 24")
        exitLabel.pack()
        exitButton = ctk.CTkButton(
            window, text="Close Window", command=lambda: window.destroy())
        exitButton.pack()
        cameraShouldStart = False

    if cameraShouldStart:
        currentTimeTable = timeTable.loc[today]

    def endAttendance() -> None:
        global cmsIDList
        dayTime = currentDate.strftime("%d-%m-%Y-%H00")
        if attendanceShouldRun:
            markAttendance(
                cmsIDList, currentTimeTable[currentDate.strftime("%H00")], dayTime)
        # global isTimerStarted
        # global shouldRunAttendance
        # isTimerStarted = False
        # shouldRunAttendance = False

        attendanceTimerThread.cancel()
        print("Attendance Done")

        window.destroy()

    attendanceDuration = 15 * SECONDS_IN_MINUTE
    attendanceTimerThread = th.Timer(attendanceDuration, endAttendance)

    if todayClassesRecord["day"] != today:
        todayClassesRecord = getDefaultAttendanceRecord(today)

    # Getting a video capture object for the camera
    if cameraShouldStart:
        capture = cv.VideoCapture(0)
        capture.set(cv.CAP_PROP_FRAME_WIDTH, 720)
        capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    def updateFrame(frame, frameContainer):
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(master=frameContainer, image=img)
        frameContainer.create_image(360, 240, image=photo)
        frameContainer.image = photo

    def printTextOnFrame(frame, text):
        if not len(frame):
            return

        cv.putText(frame, text,
                   (50, 50),  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv.LINE_AA)
        updateFrame(frame, cameraFeedContainer)

    def getCMSIdFor(encoding):
        matches = face_recognition.compare_faces(
            knownEncodings.tolist(), encoding, tolerance=0.435)
        if True not in matches:
            return None

        indexOfMatched = matches.index(True)
        return knownEncodings.index[indexOfMatched]

    def displayMarkerOnFace(frame, face, cmsId):
        top, right, bottom, left = [coord * 4 for coord in face]
        font = cv.FONT_HERSHEY_DUPLEX
        text = "Unknown" if cmsId is None else cmsId
        cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv.rectangle(frame, (left, bottom-35),
                     (right, bottom), (0, 255, 0), cv.FILLED)
        cv.putText(frame, text, (left + 6,
                                 bottom - 6), font, 1.0, (255, 255, 255), 1)

    knownEncodings = getKnownEncodings()

    def mainLoop() -> None:
        global isTimerStarted
        global attendanceShouldRun
        time = datetime.now()
        currentClassTime = time.strftime("%H00")

        if currentTimeTable[currentClassTime] is None:
            frame = getFrameInRGB(capture)
            printTextOnFrame(frame, "No class during this time slot.")
            return

        if todayClassesRecord[currentClassTime] == 0 and not isTimerStarted:
            global cmsIDList
            cmsIDList = []
            attendanceTimerThread.start()
            todayClassesRecord[currentClassTime] = 1
            isTimerStarted = True
            attendanceShouldRun = True

        if attendanceShouldRun:
            frame = getFrameInRGB(capture)
            if not len(frame):
                return

            smallFrame = cv.resize(frame, (0, 0), fy=0.25, fx=0.25)
            faces = face_recognition.face_locations(smallFrame)

            if len(faces) != 1:
                printTextOnFrame(
                    frame, "Ensure that there is one person in front of camera.")
                updateFrame(frame, cameraFeedContainer)
                return

            currentFace = faces[0]
            face_encoding = face_recognition.face_encodings(
                smallFrame, faces)[0]
            cmsId = getCMSIdFor(face_encoding)
            displayMarkerOnFace(frame, currentFace, cmsId)
            print(cmsId, cmsIDList)
            if cmsId and cmsId not in cmsIDList:
                cmsIDList.append(cmsId)

            updateFrame(frame, cameraFeedContainer)
        else:
            frame = getFrameInRGB(capture)
            printTextOnFrame(frame, "Attendance Already Done")

    def addStateToJSON(file, data):
        with open(file, 'w') as f:
            json.dump(data, f)

    def closeWindow():
        addStateToJSON('attendanceVariables.json', todayClassesRecord)
        capture.release()
        endAttendance()
        # attendanceTimerThread.cancel()
        print(cmsIDList)

    cameraFeedContainer = tk.Canvas(window, width=720, height=480)
    cameraFeedContainer.pack()

    terminateButton = ctk.CTkButton(
        window, text="Terminate", command=closeWindow)
    terminateButton.pack()

    delay = 1

    def startCamera():
        mainLoop()
        window.after(delay, startCamera)

    if cameraShouldStart:
        startCamera()

    window.protocol("WM_DELETE_WINDOW", closeWindow)
    window.mainloop()


if __name__ == "__main__":
    main()
