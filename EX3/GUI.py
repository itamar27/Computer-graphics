from tkinter import *
from tkinter import font as tkFont

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
    
    def __init__(self):
        '''
        Initial GuI and logical elements of the program
        '''
        # create  graphical interface elements
        fileBtn = Button(self.window, text="Open file",  command= self.openFile,
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

    def openFile(self):
        coords, polygons = FileManager().openFile()
        self.data = Data(coords, polygons)
        # NOTE: so far we have created polygons inside the Data object from the file read.
        self.draw('Perspective')


    def draw(self,type_projection):
        polygons = self.data.getPolygons(type_projection)
        height_mid = self.height / 2
        width_mid = self.width / 2
        for poly in polygons:
            for i,p in enumerate(poly):
                cord = []
                cord.append(p[0] + width_mid)
                cord.append(p[1] + height_mid)
                poly[i] = tuple(cord)
                print(p)
            self.canvas.create_polygon(poly,fill='#ffffff',outline='#000000')