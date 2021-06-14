from tkinter import *
<<<<<<< Updated upstream
from tkinter import font as tkFont
import time
=======
from tkinter import font as tkFont, colorchooser
import regex as re
>>>>>>> Stashed changes

# self created libaries
from file_utils import FileManager
from advances_shape_utils import *


class GUI:

    # Logical class variables

    # UI elements
    width = 1200
    height = 800
    color = 'white'
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
<<<<<<< Updated upstream
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
=======
        # Creating the top bar navigation
        self.data = None
        helpmenu = Menu(self.menuHelp)
        self.menuHelp.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About",command=self.about_command)
        helpmenu.add_command(label="User guide",command=self.help_command)


        # create  graphical interface elements
        fileBtn = Button(self.window, text="Open file",  command=self.openFile,
                         height=4, width=30, bg='SkyBlue2', fg='white', font=self.helv36)
        zoomInBtn = Button(self.window, text="Zoom in", command=lambda: self.scale("in"),
                           height=4, width=30, bg='SkyBlue2', fg='white', font=self.helv36)
        zoomOutBtn = Button(self.window, text="Zoom out", command=lambda: self.scale("out"),
                            height=4, width=30, bg='SkyBlue2', fg='white', font=self.helv36)
        rotateBtnX = Button(self.window, text="Rotate X",command=lambda:self.popUpRotate("x"),
                           height=4, width=30, bg='SkyBlue2', fg='white', font=self.helv36)
        rotateBtnY = Button(self.window, text="Rotate Y",command=lambda:self.popUpRotate("y"),
                            height=4, width=30, bg='SkyBlue2', fg='white', font=self.helv36)
        rotateBtnZ = Button(self.window, text="Rotate Z",command=lambda:self.popUpRotate("z"),
                            height=4, width=30, bg='SkyBlue2', fg='white', font=self.helv36)
        clearBtn = Button(self.window, text="Clear Screen",  command=self.clearCanvas,
                          height=4, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        self.msgText = Label(self.window, height=9, width=20, bg="white")

        # top buttons
        color_button = Button(self.menuTop, text='Select Color',command=self.choose_color,
                              height=2, width=15, bg='SkyBlue4', fg='white', font=self.helv36)
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        rotateBtn.pack(side=TOP)
        helpBtn.pack(side=TOP)
=======
        rotateBtnX.pack(side=TOP)
        rotateBtnY.pack(side=TOP)
        rotateBtnZ.pack(side=TOP)
        clearBtn.pack(side=TOP)
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
            self.canvas.create_polygon(poly, fill='#ffffff', outline='#000000')
            self.presentMessage(
                "Projection type:\n{}\n".format(type_projection))
=======
            self.canvas.create_polygon(poly, fill=self.color, width= 2,outline='#000000')
            self.presentMessage("Projection type:\n{}\n".format(type_projection))

    def is_number_regex(self,s):
        """ Returns True is string is a number. """
        if re.match("^-?[0-9]\d*(\.\d+)?$", s) is None:
            return s.isdigit()
        return True
>>>>>>> Stashed changes

    def scale(self, mode):
        self.data.scale(mode)
        self.draw(self.type_projection)

