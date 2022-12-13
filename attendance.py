import tkinter as tk
import csv                                                              #imported csv for reading csv files
import os                                                               #imported os for getting name of files in directory
import pandas as pd                                                     #imported pandas to make series

from config import*                                                     #imported config to get file paths

def main():
    window = tk.Tk()
    window.title("Start Attendance")
    window.geometry('720x520')

    tk.Label(master=window, text='ahmed is not changing the stuff',
             font='Arial 20 roman normal').pack()

    def getCSV(filename):                                               #function for getting encodings from csv files
        with open(f"./{directoryName}/{filename}") as f:
            reader = csv.reader(f)
            encodings = []
            for code in reader:
                encodings.extend(code)
            encodings = [float(code) for code in encodings]
            return encodings

    knownEncodingFiles = os.listdir(f"./{directoryName}")               #Getting names of all csv files in directory
    encodings=[]                                                        #variable definition
    encodingPrimaryKey=[]                                               #variable definition
    for file in knownEncodingFiles:                                     #Looping over the files to extract encodings
        encodings.append(getCSV(file))                                  #Saving encodings in encodins list
        encodingPrimaryKey.append(file[0:len(file)-4])                  #Saving Encoding primary keys
    
    encodings = pd.Series(encodings, encodingPrimaryKey)                #Creating series of encodings with proper primary keys 

    print(encodings)                                                    #printing encodings series

    tk.Label(master=window, text=getCSV("4221.csv"), font='Arial 20 roman normal').pack()

    window.mainloop()


if __name__ == "__main__":                                              #Added temporarily
    main()
