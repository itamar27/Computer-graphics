# Imports
from Canvas_painter import *
from tkinter import  *

# Tkinter global values
width = 1200
height = 900
buttonWidth = int(0.012 * width)
buttonHeight = int(0.006 * height)
window = Tk()
window.geometry('{}x{}'.format(width, height))
window.title('Exercise 2')
canvas = Canvas(window, width=width, height=0.87*height, bg='#ffffff')

# Global environment variables
mode = "None"
point = []
clicks = 0
point_index = 0

# FUNCTIONS
def setUpGraphicalEnv():
    '''
    Declaring on all the UI elements and packing them to the canvas
    '''
    global buttonWidth

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
                         width=buttonWidth, height=buttonHeight, font=("Arial", 12), command=lambda: readCoordinates(width, 0.87*height, canvas))
    clear_button = Button(button_frame, text="Clear",
                          width=buttonWidth, height=buttonHeight, font=("Arial", 12), command=lambda: clearCanvas(canvas))
    trans_button = Button(button_frame, text="Translation",
                          width=buttonWidth, height=buttonHeight, font=("Arial", 12), command=lambda: set_trans(mode_label, help_label))
    scale_button = Button(button_frame, text="Scale",
                          width=buttonWidth, height=buttonHeight, font=("Arial", 12), command=lambda: set_scale(mode_label, help_label))
    mirror_button = Button(button_frame, text="Mirror",
                           width=buttonWidth, height=buttonHeight, font=("Arial", 12), command=lambda: set_mirror(mode_label, help_label))
    rotate_button = Button(button_frame, text="Rotate",
                           width=buttonWidth, height=buttonHeight, font=("Arial", 12), command=lambda: set_rotate(mode_label, help_label))
    shear_button = Button(button_frame, text="Shear",
                           width=buttonWidth, height=buttonHeight, font=("Arial", 12), command=lambda: set_shearing(mode_label, help_label))
    quit_button = Button(button_frame, text="Quit",
                         width=buttonWidth, height=buttonHeight, font=("Arial", 12), command=lambda: quitBut())

    # Packing up UI environment
    help_label.pack()
    canvas.pack()
    mode_label.pack()
    load_coords.pack(side="left")
    trans_button.pack(side="left")
    scale_button.pack(side="left")
    mirror_button.pack(side="left")
    rotate_button.pack(side="left")
    shear_button.pack(side="left")
    clear_button.pack(side="left")
    quit_button.pack(side="left")
    button_frame.pack(side="bottom")

    # Defining canvas click functionality
    canvas.bind("<Button-1>", mouse_click)
    canvas.pack()
    # Run app gui
    window.mainloop()

def quitBut():
    global window,canvas
    window.destroy()
    window = 0
    canvas = 0

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
    global point_index, point, mode
    point = [event.x, event.y]
    
    #starts drawing, based on points num and mode
    if (mode == "translation"):
        drawTrans()

def setText(mode_label, help_label, mode, help):
    mode_label['text'] = "Drawing Mode : {} ".format(mode)
    help_label['text'] = help

###############################
###          Shear          ###
###############################
def set_shearing(mode_label, help_label):

    # Generate addition text to action
    help = "Enter x and y shearing values:"
    setText(mode_label, help_label, 'Shear', help)

    # Do the scaling
    popUpShear()

def popUpShear():
    '''
    This function generates input needed for the transformation
    '''
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(window)
    newWindow.title("Shear paint")

    # sets the geometry of toplevel
    newWindow.geometry("400x200")

    # A Label widget to show in toplevel
    Label(newWindow,
          text="Please enter the values for the shearing:").pack()

    Label(newWindow,
          text="\nEnter X value (0 for no change):").pack()
    xShear = Entry(newWindow)
    xShear.pack()

    Label(newWindow,
        text="Enter Y value (0 for no change):").pack()
    yShear = Entry(newWindow)
    yShear.pack()

    # Packing a button to the new window
    Button(newWindow, text="Shear", command=lambda: shearTranform(xShear, yShear, newWindow),
           height=2, width=10, bg='SkyBlue4', fg='white').pack(side=BOTTOM, pady=15)

def shearTranform(xShear, yShear, newWindow):
    '''
    Transformation for shearing
    '''
    shearPainting(canvas, float(xShear.get()), float(yShear.get()))


###############################
###          MIRROR         ###
###############################

def set_mirror(mode_label, help_label):
    # Generate addition text to action
    global mode
    mode = "mirror"
    help = "Click on the button for the mirroring direction"
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
    newWindow.title("Mirror paint")

    # sets the geometry of toplevel
    newWindow.geometry("400x350")

    # A Label widget to show in toplevel
    Label(newWindow,
          text="Please choose the direction you would like to mirror the paint to:").pack()

    # Packing a button to the new window
    Button(newWindow, text="Up", command=lambda: mirrorTranform("Up" ,newWindow),
           height=2, width=10, bg='SkyBlue4', fg='white').pack(pady=5)
    Button(newWindow, text="Down", command=lambda: mirrorTranform("Down" ,newWindow),
           height=2, width=10, bg='SkyBlue4', fg='white').pack(pady=5)
    Button(newWindow, text="Left", command=lambda: mirrorTranform("Left" ,newWindow),
           height=2, width=10, bg='SkyBlue4', fg='white').pack(pady=5)
    Button(newWindow, text="Right", command=lambda: mirrorTranform("Right" ,newWindow),
           height=2, width=10, bg='SkyBlue4', fg='white').pack(pady=5)
    Button(newWindow, text="Flip", command=lambda: mirrorTranform("Flip" ,newWindow),
           height=2, width=10, bg='SkyBlue4', fg='white').pack(pady=5)
    Button(newWindow, text="FlipBack", command=lambda: mirrorTranform("FlipBack" ,newWindow),
           height=2, width=10, bg='SkyBlue4', fg='white').pack(pady=5)

def mirrorTranform(direction, newWindow):
    '''
    Transformation for scaling
    '''
    mirrorPainting(canvas, direction)

###############################
###          SCALE          ###
###############################
def set_scale(mode_label, help_label):
    # Generate addition text to action
    global mode
    mode = "scale"
    help = "Enter the new scale for the painting"
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
          text="Please choose the measure you would like to multiply the paint size with:").pack()

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

###############################
###      Translation        ###
###############################
def set_trans(mode_label, help_label):
    global canvas,mode
    mode = 'translation'
    help = "Click on point on the screen to make the drawing translation"
    setText(mode_label, help_label, "Translation", help)

## draw all transformations and send to them mouse clicks
def drawTrans():
    global mode
    if mode == 'translation':
        translationPainting(point[0], point[1], canvas)

###############################
###      Rotate             ###
###############################
def set_rotate(mode_label,help_label):
    global mode
    help = "Enter the degrees for rotating the paiting"
    mode = "rotate"
    setText(mode_label, help_label, "Rotate", help)
    popUpRotate()

def popUpRotate():
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
          text="Please choose rotate degree:").pack()

    newScale = Entry(newWindow)
    newScale.pack()

    # Packing a button to the new window
    Button(newWindow, text="Confirm", command=lambda: rotateTranform(newScale, newWindow),
           height=2, width=10, bg='SkyBlue4', fg='white').pack(side=BOTTOM, pady=15)

def rotateTranform(dagree, newWindow):
    '''
    Transformation for rotate
    '''
    rotatePainting(float(dagree.get()),canvas)



