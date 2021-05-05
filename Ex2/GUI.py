# Imports
from tkinter import *
from tkinter import font as tkFont
from Canvas_painter import *
from FileManager import *

# Tkinter global values
width = 1080
height = 900
window = Tk()
window.geometry('{}x{}'.format(width, height))
window.title('Exercise 2')
canvas = Canvas(window, width=width, height=0.87*height, bg='#ffffff')

# Global environment variables
mode = "None"
points = []
clicks = 0


# FUNCTIONS
def setUpGraphicalEnv():
    '''
    Declaring on all the UI elements and packing them to the canvas
    '''
    # Customize windows look
    customizeWindow()

    # Build frames
    help_frame = Frame(window).pack(side="top")
    mode_frame = Frame(window).pack(side="bottom")
    button_frame = Frame(window)

    # Defining window labels
    help_label = Label(help_frame, text="Welcome!", font=("Arial", 20))
    mode_label = Label(
        mode_frame, text="Drawing Mode : None",  font=("Arial", 12))

    # Defining window elements
    load_coords = Button(button_frame, text="Choose File",
                         width=16,  command=lambda: readCoordinates(width, 0.87*height, canvas))
    clear_button = Button(button_frame, text="Clear",
                          width=16, command=lambda: clearCanvas(canvas))
    trans_button = Button(button_frame, text="Translation",
                          width=16, command=lambda: set_trans(mode_label, help_label))
    scale_button = Button(button_frame, text="Scale",
                          width=16, command=lambda: set_scale(mode_label, help_label))
    mirror_button = Button(button_frame, text="Mirror",
                           width=16, command=lambda: set_mirror(mode_label, help_label))
    rotate_button = Button(button_frame, text="Rotate",
                           width=16, command=set_rotate)

    # Packing up UI environment
    help_label.pack()
    canvas.pack()
    mode_label.pack()
    load_coords.pack(side="left")
    trans_button.pack(side="left")
    scale_button.pack(side="left")
    mirror_button.pack(side="left")
    rotate_button.pack(side="left")
    clear_button.pack(side="left")
    button_frame.pack(side="bottom")

    # Defining canvas click functionality
    canvas.bind("<Button-1>", mouse_click)

    # Run app gui
    window.mainloop()


def customizeWindow():
    '''
    Defining a Finer window visualization
    '''
    line_color_text = StringVar()
    line_color_text.set("#ffffff")
    curve_guide = IntVar()
    click_circle = IntVar()
    mirror_axis = StringVar()
    mirror_axis.set('x')


def mouse_click(event):
    global clicks, points

    if(clicks < 2):
        points.append([event.x, event.y])
        clicks += 1


def set_shearing():
    global mode
    mode = "shearing"
    init_draw()


def set_rotate():
    global mode
    mode = "rotate"
    help_text['text'] = "Click on 3 points on the screen to make a line. The first line is the origin, and the other 2 decide the angle"
    init_draw()


def setText(mode_label, help_label, mode, help):
    mode_label['text'] = "Drawing Mode : {} ".format(mode)
    help_label['text'] = help

###############################
###          MIRROR         ###
###############################


def set_mirror(mode_label, help_label):

    # Generate addition text to action
    help = "Enter the pop up window the desired mirror transformation:"
    setText(mode_label, help_label, "Mirror", help)

    # open window input for mirroring
    popUpMirror()

def popUpMirror():
    '''
    This function generates input needed for the transformation
    '''
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(window)
    newWindow.title("Resize paint")

    # sets the geometry of toplevel
    newWindow.geometry("400x200")

    # A Label widget to show in toplevel
    Label(newWindow,
          text="Please choose mirror direction").pack()

    scrollbar = Scrollbar(newWindow).pack()
    mylist = Listbox(newWindow, yscrollcommand= scrollbar.set)
    tmp = ['left', 'top', 'right', 'flip']
    for side in tmp:
        mylist.append(END, side)
    mylist.pack(side= "left", fill= BOTH)
    scrollbar.config(command = mylist.yview)

    # Packing a button to the new window
    Button(newWindow, text="Confirm", command=lambda: mirror(newWindow),
           height=2, width=10, bg='SkyBlue4', fg='white').pack(side=BOTTOM, pady=15)

def mirrorTranform(newWindow):
    '''
    Transformation for scaling
    '''
    # scalePainting(canvas, float(newScale.get()))
    newWindow.destroy()


###############################
###          SCALE          ###
###############################
def set_scale(mode_label, help_label):

    # Generate addition text to action
    help = "Enter new paint measure in box"
    setText(mode_label, help_label, 'Scale', help)

    # Do the scaling
    popUpScale()

def popUpScale():
    '''
    This function generates input needed for the transformation
    '''
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(window)
    newWindow.title("Resize paint")

    # sets the geometry of toplevel
    newWindow.geometry("400x200")

    # A Label widget to show in toplevel
    Label(newWindow,
          text="Please choose the measure you would like to resize the paint:").pack()

    newScale = Entry(newWindow)
    newScale.pack()

    # Packing a button to the new window
    Button(newWindow, text="Confirm", command=lambda: scaleTranform(newScale, newWindow),
           height=2, width=10, bg='SkyBlue4', fg='white').pack(side=BOTTOM, pady=15)


def scaleTranform(newScale, newWindow):
    '''
    Transformation for scaling
    '''
    scalePainting(canvas, float(newScale.get()))
    newWindow.destroy()


###############################
###      Translation        ###
###############################
def set_trans(mode_label, help_label):
    # prepare text
    help = "Click on 2 points on the screen to make the drawing in the direction and distance"
    setText(mode_label, help_label, "Translation", help)

    # Do the translation
    print(points)
