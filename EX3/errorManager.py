###
# Students name:
# Sivan Salzmann - 207056334
# Barak Daniel - 204594329
# Itamer Yarden - 204289987
###
### This module is responsible for all the errors and thier pop on the UI window/

from tkinter import messagebox

def showMsg(msg):
    '''
    Display error message to the main window panel   
    '''
    messagebox.showinfo("Error!", msg)


