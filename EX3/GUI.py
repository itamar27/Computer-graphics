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
    type_projection = 'Oblique'

    menuTop = Frame(window)
    menuHelp = Menu(window)
    window.config(menu=menuHelp)



    def __init__(self):
        '''
        Initial GuI and logical elements of the program
        '''
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

        clearBtn = Button(self.window, text="Clear Screen",  command=lambda: self.canvas.delete('all'),
                          height=4, width=30, bg='SkyBlue2', fg='white', font=self.helv36)

        self.msgText = Label(self.window, height=9, width=20, bg="white")

        # top buttons
        color_button = Button(self.menuTop, text='Select Color',command=self.choose_color,
                              height=2, width=15, bg='SkyBlue4', fg='white', font=self.helv36)

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

        # helpBtn.pack(side=TOP)

        # packing menu top
        color_button.pack(side=LEFT)
        orthographic_btn.pack(side=LEFT)
        oblique_btn.pack(side=LEFT)
        perspective_btn.pack(side=LEFT)

        self.msgText.pack(side=TOP, pady=10)

    def about_command(self):
        showinfo("Window", " 3D transforemations \n\n This program was written by: \n Sivan salzmann - 207056334 \n Itamer Yarden - 204289987 \n Barak Daniel - 204594329 \n")

    def help_command(self):
        showinfo("Window", "Help window")

    # Color picker
    def choose_color(self):
        self.color = colorchooser.askcolor(title="choose color")[1]

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
            self.canvas.create_polygon(poly, fill='#ffffff', outline=self.color)
            self.presentMessage(
                "Projection type:\n{}\n".format(type_projection))

    def is_number_regex(self,s):
        """ Returns True is string is a number. """
        if re.match("^\d+?\.\d+?$", s) is None:
            return s.isdigit()
        return True

    def scale(self, mode):
        self.data.scale(mode)
        self.draw(self.type_projection)

    def popUpRotate(self,direction):
        '''
       This function generates input needed for the transformation
       '''
        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(self.window)
        newWindow.title("Resize paint")

        # sets the geometry of toplevel
        newWindow.geometry("200x200")

        # A Label widget to show in toplevel
        Label(newWindow,text="Please choose rotate degree:").pack()

        angle = Entry(newWindow)
        angle.pack()

        # Packing a button to the new window
        Button(newWindow, text="Confirm", command=lambda: self.rotation(direction, angle),
               height=2, width=10, bg='SkyBlue4', fg='white').pack(side=BOTTOM, pady=15)

    def rotation(self, direction,angle):
        if self.is_number_regex(angle.get()) :
            self.data.rotation(direction,float(angle.get()))
            self.draw(self.type_projection)
        else:
            showMsg("Please enter only numbers!")
            return

