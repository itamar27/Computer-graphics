from tkinter import *
from tkinter import font as tkFont
import time

# self created libaries
from file_utils import FileManager
from advances_shape_utils import *


class GUI:

    # Logical class variables

    # UI elements
    width = 1200
    height = 800
    color = '#000000'
    window = Tk()
    window.geometry('{}x{}'.format(width, height))
    window.title('Exercise 3')
    window.configure(background='SkyBlue3')
    canvas = Canvas(window, width=width-200, height=height, bg="white")
    helv36 = tkFont.Font(family='Helvetica', size=10, weight='bold')
    type_projection = 'Oblique'

    menuTop = Frame(window)

    def __init__(self):
        '''
        Initial GuI and logical elements of the program
        '''
        # create  graphical interface elements
        fileBtn = Button(self.window, text="Open file",  command=self.openFile,
                         height=5, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        clearBtn = Button(self.window, text="Clear Screen",  command=lambda: self.canvas.delete('all'),
                          height=5, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        zoomInBtn = Button(self.window, text="Zoom in", command=lambda: self.scale("in"),
                           height=5, width=30, bg='SkyBlue2', fg='white', font=self.helv36)
        zoomOutBtn = Button(self.window, text="Zoom out", command=lambda: self.scale("out"),
                            height=5, width=30, bg='SkyBlue2', fg='white', font=self.helv36)
        rotateBtn = Button(self.window, text="Rotate",
                           height=5, width=30, bg='SkyBlue2', fg='white', font=self.helv36)
        helpBtn = Button(self.window, text="Help",
                         height=5, width=30, bg='SkyBlue2', fg='white', font=self.helv36)
        self.msgText = Label(self.window, height=9, width=20, bg="white")

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
        zoomInBtn.pack(side=TOP)
        zoomOutBtn.pack(side=TOP)
        rotateBtn.pack(side=TOP)
        helpBtn.pack(side=TOP)

        # packing menu top
        orthographic_btn.pack(side=LEFT)
        oblique_btn.pack(side=LEFT)
        perspective_btn.pack(side=LEFT)

        self.msgText.pack(side=TOP, pady=10)

    def presentMessage(self, msg=""):
        self.msgText['text'] = msg

    def createBoard(self):
        self.window = mainloop()

    def openFile(self):
        coords, polygons = FileManager().openFile()
        self.data = Data(coords, polygons)
        self.draw(self.type_projection)

    def draw(self, type_projection):
        self.canvas.delete('all')
        self.type_projection = type_projection
        polygons = self.data.getPolygons(type_projection)
        height_mid = int(self.height / 4)
        width_mid = int(self.width / 4)

        for poly in polygons:
            for i, p in enumerate(poly):
                cord = []
                cord.append(p[0] + width_mid)
                cord.append(p[1] + height_mid)
                poly[i] = tuple(cord)
            self.canvas.create_polygon(poly, fill='#ffffff', outline='#000000')
            self.presentMessage(
                "Projection type:\n{}\n".format(type_projection))

    def scale(self, mode):
        self.data.scale(mode)
        self.draw(self.type_projection)

