from tkinter import *
from tkinter import font as tkFont

#self created libaries
from file_utils import FileManager

class GUI:
    
    #Logical class variables
    fileManager = FileManager()

    #UI elements
    width = 1100
    height = 700
    color = '#000000'
    window = Tk()
    window.geometry('{}x{}'.format(width, height))
    window.title('Exercise 2')
    window.configure(background='SkyBlue3')
    canvas = Canvas(window, width=width-200, height=height, bg="white")
    helv36 = tkFont.Font(family='Helvetica', size=10, weight='bold')


    
    def __init__(self):
        '''
        Initial GuI and logical elements of the program
        '''
        # create  graphical interface elements
        fileBtn = Button(self.window, text="Open file",  command= self.fileManager.openFile,
                         height=6, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        clearBtn = Button(self.window, text="Clear Screen",  # command=lambda: clearCanvas(canvas),
                          height=6, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        scaleBtn = Button(self.window, text="Scale",
                             height=6, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        rotateBtn = Button(self.window, text="Rotate",
                                height=6, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        helpBtn = Button(self.window, text="Help",
                           height=6, width=30, bg='SkyBlue2', fg='white', font=self.helv36)
        self.msgText = Label(self.window, height=9, width=20, bg = "white")

        # packing all window elements
        self.canvas.pack(side=RIGHT)
        fileBtn.pack(side=TOP)
        clearBtn.pack(side=TOP)
        scaleBtn.pack(side=TOP)
        rotateBtn.pack(side=TOP)
        helpBtn.pack(side=TOP)
        self.msgText.pack(side=TOP, pady= 10)
        

    def presentMessage(self,msg=""):
        self.msgText['text'] = msg


    def createBoard(self):
        self.window = mainloop()
