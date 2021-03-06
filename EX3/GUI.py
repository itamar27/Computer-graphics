###
# Students name:
# Sivan Salzmann - 207056334
# Barak Daniel - 204594329
# Itamer Yarden - 204289987
###
from tkinter import *
from tkinter import font as tkFont, colorchooser

# self created libaries
from tkinter.messagebox import showinfo
from file_utils import FileManager
from advances_shape_utils import *
from errorManager import showMsg

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
    type_projection = 'Orthographic'

    menuTop = Frame(window, bg="SkyBlue3")
    menuHelp = Menu(window)
    window.config(menu=menuHelp)

    def __init__(self):
        '''
        Initial GuI and logical elements of the program
        '''
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

        rotateBtnX = Button(self.window, text="Rotate X",command=lambda: self.rotation("x", angle),
                           height=4, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        rotateBtnY = Button(self.window, text="Rotate Y",command=lambda:self.rotation("y", angle),
                            height=4, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        rotateBtnZ = Button(self.window, text="Rotate Z",command=lambda: self.rotation("z", angle),
                            height=4, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        clearBtn = Button(self.window, text="Clear Screen",  command=self.clearCanvas,
                          height=4, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        closeBtn = Button(self.window, text="Quit",  command=self.closeProg,
                          height=4, width=30, bg='SkyBlue4', fg='white', font=self.helv36)

        self.msgText = Label(self.window, height=9, width=20, bg="white")

        # top buttons
        rotateLabel = Label(self.menuTop,text="Rotation degree(default=15):", bg='SkyBlue3', height=3, font=self.helv36)
        angle = Entry(self.menuTop)

        color_button = Button(self.menuTop, text='Select Color',command=self.choose_color,
                              height=2, width=15, bg='SkyBlue3', fg='white', font=self.helv36)

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
        zoomInBtn.pack(side=TOP)
        zoomOutBtn.pack(side=TOP)
        rotateBtnX.pack(side=TOP)
        rotateBtnY.pack(side=TOP)
        rotateBtnZ.pack(side=TOP)
        clearBtn.pack(side=TOP)
        closeBtn.pack(side=TOP)

        # packing menu top
        rotateLabel.pack(side=LEFT)
        angle.pack(side=LEFT, padx=15)
        color_button.pack(side=LEFT)
        orthographic_btn.pack(side=LEFT)
        oblique_btn.pack(side=LEFT)
        perspective_btn.pack(side=LEFT)

        self.msgText.pack(side=TOP, pady=10)

    def clearCanvas(self):
        ''' Clear the canvas to start over '''
        self.canvas.delete("all")
        self.data = None
        showMsg("All clear! Let's start again.")
    
    def closeProg(self):
        ''' Close the program button '''
        self.window.destroy()
        self.window = 0
        self.canvas = 0


    def about_command(self):
        showinfo("About", " 3D transforemations \n\n This program was written by: \n Sivan salzmann - 207056334 \n Itamer Yarden - 204289987 \n Barak Daniel - 204594329 \n")

    def help_command(self):
        showinfo("Help", "Welcome to our Project-3D software! \n\n For using our interface you must follow these steps:\n\n1. You need to open a coordinate file, we have provided you with the polygons.txt file and it is recommended to use it!\n\n2. After opening the file, you must select the desired projection or use the default projection we provided you.\n\n3. You can choose to make transformations:\nZoom in\nZoom out\nRotation X\nRotation Y\nRotation Z\n\n4. You have the option to choose to change the fill color of the shapes from black to any color you want by clicking select color.\n\n5. You can quickly delete all information from the screen and restart at any time by clicking Clear screen.\n\n6. To exit the program, click Quite.\n\nhave a nice time!")

    # Color picker
    def choose_color(self):
        self.color = colorchooser.askcolor(title="choose color")[1]
        self.draw(self.type_projection)

    def presentMessage(self, msg=""):
        self.msgText['text'] = msg

    def createBoard(self):
        self.window = mainloop()

    def openFile(self):
        ''' This function open the file in the gui and set the daata into Data
            object. After it all set the data will draw on the screen.'''
        coords, polygons = FileManager().openFile()
        if coords == [] or polygons == []:
            showMsg("File input is invalid please enter another file!")
            return
        self.data = Data(coords, polygons)
        self.draw(self.type_projection)

    def draw(self, type_projection):
        ''' Draw the data on the screen after the window is clear
            the sizes of the window is affect on the polygons state
            on the screen. '''
        self.canvas.delete('all')
        self.type_projection = type_projection
        if self.data == None:
            showMsg("Please open file first!")
            return

        polygons = self.data.getPolygons(type_projection)
        height_mid = int(self.height / 2.2)
        width_mid = int(self.width / 2.2)

        for poly in polygons:
            for i, p in enumerate(poly):
                cord = []
                cord.append(int(p[0] + width_mid))
                cord.append(int(p[1] + height_mid))
                poly[i] = tuple(cord)
            # create each polygon. fill the polygon by user choosing color.
            self.canvas.create_polygon(poly, fill=self.color, width= 2,outline="#ffffff")
            self.presentMessage("Projection type:\n{}\n".format(type_projection))

    def is_number_regex(self,s):
        """ Returns True is string is a number. """
        if re.match("^-?[0-9]\d*(\.\d+)?$", s) is None:
            return s.isdigit()
        return True

    def scale(self, mode):
        ''' Scale transformation '''
        if self.data == None:
            showMsg("Please open file first!")
            return
        self.data.scale(mode)
        self.draw(self.type_projection)

    def rotation(self, direction,angle):
        ''' Rotation transformation '''
        if self.data == None:
            showMsg("Please open file first!")
            return
        if angle.get() == "":
            self.data.rotation(direction,float(15))
            self.draw(self.type_projection)
        elif self.is_number_regex(angle.get()) :
            self.data.rotation(direction,float(angle.get()))
            self.draw(self.type_projection)
        else:
            showMsg("Please enter only numbers!")
            return

