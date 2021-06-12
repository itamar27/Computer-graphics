from tkinter import *
from tkinter import font as tkFont
import time

#self created libaries
from file_utils import FileManager
from advances_shape_utils import *

class GUI:
    
    #Logical class variables

    #UI elements
    width = 1100
    height = 700
    color = '#000000'
    window = Tk()
    window.geometry('{}x{}'.format(width, height))
    window.title('Exercise 3')
    window.configure(background='SkyBlue3')
    canvas = Canvas(window, width=width-200, height=height, bg="white")
    helv36 = tkFont.Font(family='Helvetica', size=10, weight='bold')

    menuTop = Frame(window)

    def __init__(self):
        '''
        Initial GuI and logical elements of the program
        '''
        # create  graphical interface elements
        fileBtn = Button(self.window, text="Open file",  command= self.openFile,
                         height=6, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        clearBtn = Button(self.window, text="Clear Screen",  command=lambda: self.canvas.delete('all'),
                          height=6, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        scaleBtn = Button(self.window, text="Scale",
                             height=6, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        rotateBtn = Button(self.window, text="Rotate",
                                height=6, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        helpBtn = Button(self.window, text="Help",
                           height=6, width=30, bg='SkyBlue2', fg='white', font=self.helv36)
        self.msgText = Label(self.window, height=9, width=20, bg = "white")

        # projections buttons
        orthographic_btn = Button(self.menuTop, text="Orthographic",  command=lambda: self.draw("Orthographic"),
                                  height=2, width=15, bg='SkyBlue2', fg='white', font=self.helv36)

        oblique_btn = Button(self.menuTop, text="Oblique",  command=lambda: self.draw("Oblique"),
                                 height=2, width=15, bg='SkyBlue2', fg='white', font=self.helv36)

        perspective_btn = Button(self.menuTop, text="Perspective",  command=lambda: self.draw("Perspective"),
                                 height=2, width=15, bg='SkyBlue2', fg='white', font=self.helv36)

        # packing all window elements
        self.menuTop.pack(side=TOP)
        self.canvas.pack(side=RIGHT)
        fileBtn.pack(side=TOP)
        clearBtn.pack(side=TOP)
        scaleBtn.pack(side=TOP)
        rotateBtn.pack(side=TOP)
        helpBtn.pack(side=TOP)

        # packing menu top
        orthographic_btn.pack(side=LEFT)
        oblique_btn.pack(side=LEFT)
        perspective_btn.pack(side=LEFT)

        self.msgText.pack(side=TOP, pady= 10)


    def presentMessage(self,msg=""):
        self.msgText['text'] = msg

    def createBoard(self):
        self.window = mainloop()

    def openFile(self):
        coords, polygons = FileManager().openFile()
        self.data = Data(coords, polygons)
        self.draw('Orthographic')


    def draw(self,type_projection):
        self.canvas.delete('all')
        polygons = self.data.getPolygons(type_projection)
        height_mid = self.height / 2
        width_mid = self.width / 2

        for poly in polygons:
            # for i,p in enumerate(poly):
            #     cord = []
            #     cord.append(p[0] + width_mid)
            #     cord.append(p[1] + height_mid)
            #     poly[i] = tuple(cord)
            self.presentMessage("Projection type: {}\n".format(type_projection))
            self.canvas.create_polygon(poly,fill='#ffffff',outline='#000000')