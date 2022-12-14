import tkinter as tk
import csv                                                              #imported csv for reading csv files
import os                                                               #imported os for getting name of files in directory
import pandas as pd                                                     #imported pandas to make series
import cv2 as cv                                                        #imported opencv for image processing
import face_recognition                                                 #imported face_recognition for recognizing images
import numpy as np                                                      #imported numpy for math functions

from PIL import Image, ImageTk                                          #
from config import*                                                     #imported config to get file paths

def main():
    window = tk.Tk()
    window.title("Start Attendance")
    window.geometry('720x520')

    capture = cv.VideoCapture(1)                                        #Getting a video capture object for the camera
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 720)                           #Width and
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)                          #Height of Camera

    #tk.Label(master=window, text='ahmed is not changing the stuff',
             #font='Arial 20 roman normal').pack()
    videoCapture = tk.Label(window)
    videoCapture.pack()

    def getCSV(filename):                                               #function for getting encodings from csv files
        with open(f"./{directoryName}/{filename}") as f:
            reader = csv.reader(f)
            encodings = []
            for code in reader:
                encodings.extend(code)
            encodings = [float(code) for code in encodings]
            return encodings

    knownEncodingFiles = os.listdir(f"./{directoryName}")               #Getting names of all csv files in directory
    encodings=pd.Series(dtype='float64')                                #series for encodings definition
    for file in knownEncodingFiles:                                     #Looping over the files to extract encodings
        encodings[file[:-4]] = getCSV(file)                             #Saving encodings in Series with proper primary keys

    print(encodings)                                                    #printing encodings series
    
    def runCamera():
        ret, frame = capture.read()                                     #Get Captured frame from Camera

        smallFrame = cv.resize(frame, (0, 0), fx=1.0, fy=1.0)
        smallFrame = cv.cvtColor(smallFrame, cv.COLOR_BGR2RGB)        

        capturedImage = Image.fromarray(smallFrame)                   # Capture the latest frame and transform to image
  
        photoImage = ImageTk.PhotoImage(image=capturedImage)          # Convert captured image to photoimage

        videoCapture.photoImage = photoImage                          # Displaying photoimage in the label
  
        videoCapture.configure(image=photoImage)                       # Configure image in the label
        window.after(1, runCamera)                          # Repeat the same process after every 10 milliseconds
    
    runCamera()
    window.mainloop()


if __name__ == "__main__":                                              #Added temporarily
    main()
