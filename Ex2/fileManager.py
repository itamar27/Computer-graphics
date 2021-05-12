# This libary handles the functionality to open file in path and read it to your application

import os
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from errorManager import showMsg

# Functions


def handleFile(name):
    '''
    This function is handling the file after being choose from the user input
    '''
    with open(name) as f:
        index = 0
        lines = []
        radiuses = []
        curves = []
        fileLines = f.read().splitlines()

        # Read all file inputs from list 
        while index < len(fileLines):
    
            if fileLines[index] == "Lines":
                index += 1
                while fileLines[index] != "#":
                    lines.append(fileLines[index])
                    index += 1
                index += 1

            elif fileLines[index] == "Radiuses":
                index += 1
                while fileLines[index] != "#":
                    radiuses.append(fileLines[index])
                    index += 1
                index += 1

            elif fileLines[index] == "Curves":
                index += 1
                while fileLines[index] != "#":
                    curves.append(fileLines[index])
                    index += 1
                index += 1

            else:
                showMsg("File input is invalid please enter another file!")
                return
        return lines, radiuses, curves


def selectFile():
    '''
    This function creating a window for selecting a file in a directory
    '''
    # choose dir
    folder_path = tk.StringVar()
    filename = askopenfilename()
    folder_path.set(filename)
    # send file path for opening
    return  handleFile(filename)

   