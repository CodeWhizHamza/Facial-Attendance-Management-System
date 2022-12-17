import tkinter as tk
import csv  # imported csv for reading csv files
import os  # imported os for getting name of files in directory
import pandas as pd  # imported pandas to make series
import cv2 as cv  # imported opencv for image processing
import face_recognition  # imported face_recognition for recognizing images
import numpy as np  # imported numpy for math functions
from tkinter import ttk
from time import sleep
from datetime import datetime
import threading as th
import json

from PIL import Image, ImageTk                                          #
from config import *  # imported config to get file paths
from helper import *

global isTimerStarted
isTimerStarted = False
global shouldRunAttendance
shouldRunAttendance = False


def main():
    window = tk.Tk()
    window.title("Start Attendance")
    window.geometry('720x520')

    isRunLoop = True

    day = ["Monday", "Tuesday", "Wednesday",
           "Thursday", "Friday", "Saturday", "Sunday"]

    with open('attendanceVariables.json', 'r') as file:
        isPeriodDone = json.load(file)

    dt = datetime.now()

    currentDay = day[dt.weekday()]

    currentTimeTable = timeTable.loc["Monday"]  # Replace with currentDay

    global cmsIDList
    cmsIDList = []

    def markTheAttendence():
        global cmsIDList
        markAttendance(cmsIDList, currentTimeTable["0900"], dt.strftime(
            "%d-%m-%Y-0900"))  # replace with dt.strftime("%H00")
        cmsIDList = []
        print("Data in table")

    def endAttendence() -> None:
        markTheAttendence()
        global isTimerStarted
        global shouldRunAttendance
        isTimerStarted = False
        shouldRunAttendance = False
        attendenceTimeThread.cancel()
        print("Attendance Done")

    timeForAttendence = 10.0  # In seconds

    attendenceTimeThread = th.Timer(timeForAttendence, endAttendence)

    # if currentDay == "Saturday" or currentDay == "Sunday":
    #     exitLable = tk.Label(
    #         window, text="It's a weekend, GO and enjoy your Weekend\n:)", font="Arial 24")
    #     exitLable.pack()
    #     exitButton = ttk.Button(
    #         window, text="Close Window", command=lambda: window.destroy())
    #     exitButton.pack()
    #     isRunLoop = False

    # elif 900 > int(dt.strftime("%H%M")) or int(dt.strftime("%H%M")) > 1700:
    #     exitLable = tk.Label(
    #         window, text="You Tried to initialize system out of class Hours.\n Please try again later -_-", font="Arial 24")
    #     exitLable.pack()
    #     exitButton = ttk.Button(
    #         window, text="Close Window", command=lambda: window.destroy())
    #     exitButton.pack()
    #     isRunLoop = False

    if isPeriodDone["day"] != "Monday":    # Replace with currentDay
        isPeriodDone["day"] = "Monday"  # Replace with currentDay
        isPeriodDone["0900"] = 0
        isPeriodDone["1000"] = 0
        isPeriodDone["1100"] = 0
        isPeriodDone["1200"] = 0
        isPeriodDone["1300"] = 0
        isPeriodDone["1400"] = 0
        isPeriodDone["1500"] = 0
        isPeriodDone["1600"] = 0

    # Getting a video capture object for the camera
    capture = cv.VideoCapture(0)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 720)  # Width and
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    def getFrame():  # Height of Camera
        ret, frame = capture.read()
        if ret:
            return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        else:
            return (ret, None)

    def printTextOnFrame(text):
        ret, frame = getFrame()
        if not ret:
            return
        cv.putText(frame, text,
                   (50, 50),  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv.LINE_AA)
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(master=videoCapture, image=img)
        videoCapture.create_image(360, 240, image=photo)
        videoCapture.image = photo  # printing encodings series

    def identifyCMSIDFromFace():
        cmsID = "0"
        # cmsID = "415216"
        # print("camera")
        ret, frame = getFrame()
        if not ret:
            return
        smallFrame = cv.resize(frame, (0, 0), fy=0.25, fx=0.25)
        face_locations = face_recognition.face_locations(smallFrame)

        if len(face_locations) == 0:
            pass
        elif len(face_locations) == 1:
            face = face_locations[0]
            frame_encoding = face_recognition.face_encodings(smallFrame, [face])[
                0]
            top, right, bottom, left = face
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv.rectangle(frame, (left, top),
                         (right, bottom), (255, 0, 0), 2)
            matches = face_recognition.compare_faces(
                knownEncodings.tolist(), frame_encoding, tolerance=0.5)
            name = "Unknown"
            font = cv.FONT_HERSHEY_DUPLEX
            if True in matches:
                cmsID = knownEncodings.index[matches.index(True)]

                cv.rectangle(frame, (left, bottom-35),
                             (right, bottom), (255, 0, 0), cv.FILLED)

                cv.putText(frame, cmsID, (left + 6, bottom - 6),
                           font, 1.0, (255, 255, 255), 1)

            else:
                cv.rectangle(frame, (left, bottom-35),
                             (right, bottom), (255, 0, 0), cv.FILLED)
                cv.putText(frame, name, (left + 6, bottom - 6),
                           font, 1.0, (255, 255, 255), 1)
        else:
            cv.putText(frame, "Please make sure one person is in front of camera.",
                       (50, 50),  cv.FONT_HERSHEY_SIMPLEX, 24, (0, 0, 255), 1, cv.LINE_AA)

        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(master=videoCapture, image=img)
        videoCapture.create_image(360, 240, image=photo)
        videoCapture.image = photo  # printing encodings series

        return cmsID

    def getCSV(filename):  # function for getting encodings from csv files
        with open(f"./{directoryName}/{filename}") as f:
            reader = csv.reader(f)
            encodings = []
            for code in reader:
                encodings.extend(code)
            encodings = [float(code) for code in encodings]
        return encodings

        # Getting names of all csv files in directory
    knownEncodingFiles = os.listdir(f"./{directoryName}")
    # series for encodings definition
    knownEncodings = pd.Series(dtype='float64')
    for file in knownEncodingFiles:  # Looping over the files to extract encodings
        knownEncodings[file[:-4]] = getCSV(file)

        # Saving encodings in Series with proper primary key

    def mainLoop() -> None:
        global isTimerStarted
        global shouldRunAttendance
        dt = datetime.now()
        currentPeriodSLot = "0900"  # add later dt.strftime("%H00")
        if currentTimeTable[currentPeriodSLot] != None:
            if not isPeriodDone[currentPeriodSLot]:
                if not isTimerStarted:
                    attendenceTimeThread.start()
                    isPeriodDone[currentPeriodSLot] = 1
                    isTimerStarted = True
                    shouldRunAttendance = True
                elif shouldRunAttendance == False:
                    exitLable = tk.Label(
                        window, text="No scheduled Class for current period :)", font="Arial 24")
                    exitLable.pack()

            if shouldRunAttendance:
                cmsID = identifyCMSIDFromFace()
                if cmsID:
                    if cmsID not in cmsIDList:
                        cmsIDList.append(cmsID)
            else:
                printTextOnFrame("Attendance Already Done")

        else:
            printTextOnFrame("Class not Scheduled for Now")

    def closeWindow():
        with open('attendanceVariables.json', 'w') as file:
            json.dump(isPeriodDone, file)
        print(cmsIDList)
        window.destroy()
        capture.release()

    videoCapture = tk.Canvas(window, width=720, height=480)
    videoCapture.pack()

    terminateButton = ttk.Button(
        window, text="Terminate", command=closeWindow)
    terminateButton.pack()

    delay = 1

    def loop():
        mainLoop()
        window.after(delay, loop)
    if isRunLoop:
        loop()

    window.mainloop()


if __name__ == "__main__":
    main()
