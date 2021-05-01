### This module is responsible for all the errors and thier pop on the UI window/

import tkinter as tk
from tkinter import messagebox

def showError(msg):
    '''
    Display error message to the main window panel   
    '''
    messagebox.showinfo("Error!", msg)


