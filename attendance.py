import tkinter as tk
import csv  # imported csv for reading csv files
import os  # imported os for getting name of files in directory
import pandas as pd  # imported pandas to make series
import cv2 as cv  # imported opencv for image processing
import face_recognition  # imported face_recognition for recognizing images
import numpy as np  # imported numpy for math functions
from tkinter import ttk
from time import sleep


from PIL import Image, ImageTk                                          #
from config import *  # imported config to get file paths


def main():
    window = tk.Tk()
    window.title("Start Attendance")
    window.geometry('720x520')

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

        # Saving encodings in Series with proper primary keys

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

    def update():
        ret, frame = getFrame()
        if not ret:
            return

        smallFrame = cv.resize(frame, (0, 0), fy=0.25, fx=0.25)

        face_locations = face_recognition.face_locations(smallFrame)

        if len(face_locations) == 0:
            print("No face detected")
        elif len(face_locations) == 1:
            face = face_locations[0]
            frame_encoding = face_recognition.face_encodings(smallFrame, [face])[
                0]

            top, right, bottom, left = face
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

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
        videoCapture.image = photo

        window.after(delay, update)  # printing encodings series

    def closeWindow():
        window.destroy()
        capture.release()

    videoCapture = tk.Canvas(window, width=720, height=480)
    videoCapture.pack()

    terminateButton = ttk.Button(
        window, text="Terminate", command=closeWindow)
    terminateButton.pack()

    delay = 1
    update()
    # print(timeTable)
    window.mainloop()


if __name__ == "__main__":
    main()
