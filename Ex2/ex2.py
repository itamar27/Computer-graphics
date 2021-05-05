# imports
from tkinter import *
from tkinter import font as tkFont
import math as math
import re
import numpy as np

# functions
def clearCanvas(canvas):
    canvas.delete("all")


def drawPixel(x, y, canvas):
    '''
    Draw one pixel on the canvas bored that the function received as an argument
    Because tkinter doesn't have any function like 'PutPixel()', we will use a manipulation on the create_rectangle methods
    '''
    canvas.create_line(x, y, x + 1, y)
    #canvas.create_rectangle((x, y) * 2, outline=colorString)


def MyLine(x0, y0, x1, y1, canvas):
    '''
    DDA implementation for drawing a line between 2 given points, (x0, y0) and (x1, y1).
    '''
    xDiff = x1 - x0
    yDiff = y1 - y0
    # marking the longer axis for the smoothening operation
    x_longer = True if abs(xDiff) > abs(yDiff) else False

    myRange = max(abs(xDiff), abs(yDiff))
    if myRange == 0:
        myRange = 1

    deltaX = (xDiff)/myRange
    deltaY = (yDiff)/myRange

    x = x0
    y = y0

    for move in range(0, myRange):
        # drawing pixel with the current values and then evaluating the next values
        drawPixel(round(x), round(y), canvas)
        oldY = y
        oldX = x
        x = x + deltaX
        y = y + deltaY

        # smoothening the line draw with more pixels when we step on the shorter axis
        if x_longer:
            if round(oldY) != round(y):
                drawPixel(round(oldX), round(y), canvas)
        else:
            if round(oldX) != round(x):
                drawPixel(round(x), round(oldY), canvas)


def drawCircle(xc, yc, x, y, canvas):
    '''
    Help function for the MyCircle() draw operation, draws a pixel for every
    1/8 of the circles outline (radius)
    '''
    drawPixel(xc+x, yc+y, canvas)
    drawPixel(xc-x, yc+y, canvas)
    drawPixel(xc+x, yc-y, canvas)
    drawPixel(xc-x, yc-y, canvas)
    drawPixel(xc+y, yc+x, canvas)
    drawPixel(xc-y, yc+x, canvas)
    drawPixel(xc+y, yc-x, canvas)
    drawPixel(xc-y, yc-x, canvas)


def MyCircle(x0, y0, radius, canvas):
    '''
    This function is drawing a circle with bezier circle algorithm,
    dividing the circle to 8 parts, that way it is more efficient.
    '''
    x = 0
    y = radius
    p = 3 - 2*radius

    while(y >= x):

        if(p > 0):
            y -= 1
            p = p + 4 * (x - y) + 10
        else:
            p = p + 4 * x + 6
        drawCircle(x0, y0, x, y, canvas)
        x += 1


def BezierCurve(coordsMatrix, canvas):
    '''
    This function is drawing the Bezier curve, choosing 4 control points
    the curve must go through the two nodes and hold its place with the other points.
    '''

    numOfLines = 100

    deltaT = 1/numOfLines

    x_coeff1 = -coordsMatrix[0][0] + 3*coordsMatrix[1][0] - \
               3*coordsMatrix[2][0] + coordsMatrix[3][0]
    x_coeff2 = 3*coordsMatrix[0][0] - 6 * \
               coordsMatrix[1][0] + 3*coordsMatrix[2][0]
    x_coeff3 = -3*coordsMatrix[0][0] + 3*coordsMatrix[1][0]
    x_coeff4 = coordsMatrix[0][0]

    y_coeff1 = -coordsMatrix[0][1] + 3*coordsMatrix[1][1] - \
               3*coordsMatrix[2][1] + coordsMatrix[3][1]
    y_coeff2 = 3*coordsMatrix[0][1] - 6 * \
               coordsMatrix[1][1] + 3*coordsMatrix[2][1]
    y_coeff3 = -3*coordsMatrix[0][1] + 3*coordsMatrix[1][1]
    y_coeff4 = coordsMatrix[0][1]

    x0 = coordsMatrix[0][0]
    y0 = coordsMatrix[0][1]

    t = deltaT
    while t < 1.01:
        x1 = int(x_coeff1*t*t*t+x_coeff2*t*t+x_coeff3*t+x_coeff4)
        y1 = int(y_coeff1*t*t*t+y_coeff2*t*t+y_coeff3*t+y_coeff4)
        # using myLine function to draw line as part of curve
        MyLine(x0, y0, x1, y1, canvas)
        x0, y0 = x1, y1
        t = t + deltaT

#window size
width = 900
height = 600
lines = []
curves = []
circles = []

#open file
with open('boat.txt') as f:
    data = f
    fileLines = data.read().splitlines()

def handleFile():
    '''
    This function is handling the file after being choose from the user input
    '''
    global lines,curves,circles,fileLines
    index = 0

    # Read all file inputs from list
    while index < len(fileLines):

        if fileLines[index] == "Lines":
            index += 1
            while fileLines[index] != "#":
                lines.append(fileLines[index])
                index += 1
            index += 1

        elif fileLines[index] == "Radiuses":
            index += 1
            while fileLines[index] != "#":
                circles.append(fileLines[index])
                index += 1
            index += 1

        elif fileLines[index] == "Curves":
            index += 1
            while fileLines[index] != "#":
                curves.append(fileLines[index])
                index += 1
            index += 1

        else:
            # showError("File input is invalid please enter another file!")
            return
    return lines, circles, curves


#tkinter global vals
window = Tk()
window.title("Exercise 2")
bg_color_text = StringVar()
bg_color_text.set("#ffffff")
canvas = Canvas(window, width = width, height = height, bg=bg_color_text.get())
line_color_text = StringVar()
line_color_text.set("#ffffff")
curve_guide = IntVar()
click_circle = IntVar()
mirror_axis = StringVar()
mirror_axis.set('x')

mode = "None"
close_flag = False
points = [[0,0], [0,0], [0,0], [0,0]]
point_index = 0

button_frame = Frame(window)

#Help Text
help_frame = Frame(window)
help_text = Label(help_frame, text="Welcome!")
help_text.pack()

#Mode Label
mode_frame = Frame(window)
mode_label = Label(mode_frame, text= "Drawing Mode : " + mode, bg=line_color_text.get())
mode_label.pack()

#Set in GUI
help_frame.pack(side = "top")
mode_frame.pack( side = "bottom" )

def clear_data():
    global data
    data = {"lines" : [], "circles": [], "curves": []}
    clear()

clear_button = Button(button_frame, text="Clear", width=16, command=clear_data)
clear_button.pack( side = "left" )


#get mouse coordinets
def mouse_click(event):
    global point_index, points, mode
    points[point_index] = [event.x, event.y]
    point_index += 1


#initilize drawing
def init_draw():
    global point_index, mode
    mode_label['text'] = "Drawing Mode : " + mode
    point_index = 0


#button functions
def set_trans():
    global mode
    mode = "trans"
    help_text['text'] = "Click on 2 points on the screen to make the drawing in the direction and distance"
    init_draw()
    draw()

def set_scale():
    global mode
    mode = "scale big"
    help_text['text'] = "Click on 2 points on the screen to make the drawing bigger"
    init_draw()
    draw()


def set_mirror():
    global mode
    mode = "mirror"
    help_text['text'] = "Click on the screen to mirror the drawing. You can change the mirror axis in the options"
    init_draw()

def set_shearing():
    global mode
    mode = "shearing"
    init_draw()

def set_rotate():
    global mode
    mode = "rotate"
    help_text['text'] = "Click on 3 points on the screen to make a line. The first line is the origin, and the other 2 decide the angle"
    init_draw()

def clear():
    init_draw()

def clear_data():
    global data
    data = {"lines" : [], "circles": [], "curves": []}
    clear()

#2D Transformation Buttons
#Create
trans_frame = Frame(window)
trans_button = Button(trans_frame, text="Translation", width=16, command=set_trans)
scaleb_button = Button(trans_frame, text="Scaling big", width=16, command=set_scale_big)
scales_button = Button(trans_frame, text="Scaling small", width=16, command=set_scale_small)
mirror_button = Button(trans_frame, text="Mirror", width=16, command=set_mirror)
rotate_button = Button(trans_frame, text="Rotate", width=16, command=set_rotate)

#Set in GUI
trans_button.pack( side = "left" )
scaleb_button.pack( side = "left" )
scales_button.pack( side = "left" )
mirror_button.pack( side = "left" )
rotate_button.pack( side = "left" )

trans_frame.pack(side = "bottom")

def createCoordinates(string):
    '''
    Parse the string from file with the token splitting the arguments
    '''
    string = string[1:-1]
    coor = string.split(',')
    return coor

def drawLines(_lines):
    '''
    receive all lines as a list and add them to the canvas
    '''
    global lines
    for line in _lines:
        split_line = createCoordinates(line)
        x1, y1, x2, y2 = split_line
        lines = split_line
        MyLine(int(x1), int(y1), int(x2), int(y2), canvas)


def drawRadiuses(radiuses):
    '''
    receive all curves as list and add them to the canvas
    '''
    global circles
    for radius in radiuses:
        split_radious = createCoordinates(radius)
        x1, y1, R ,size = split_radious
        circles = split_radious
        MyCircle(int(x1), int(y1), int(size), canvas)


def drawCurves(_curves):
    '''
    receive all curves that are part of the main drawing and add them to the canvas
    '''
    global curves
    for curve in _curves:
        split_curve = createCoordinates(curve)
        x1, y1, x2, y2, x3, y3, x4, y4 = split_curve
        coordsMatrix = [[int(x1), int(y1)], [int(x2), int(y2)], [
            int(x3), int(y3)], [int(x4), int(y4)]]
        curves = split_curve
        BezierCurve(coordsMatrix, canvas)

def readCoordinates():
    '''
    Getting Cordinates from the file input,
    then scaling the vectors to our window size,
    then painting the data to the window.
    '''
    global lines, circles, curves
    # currLines, currRadiuses, currCurves = select_file()
    lines, circles, curves = handleFile()

    drawLines(lines)
    drawRadiuses(circles)
    drawCurves(curves)


def scaleCanvas(newscale=0.5):
    '''
    Scales the canvas paiting by a given scale, defualt is 0.5
    '''
    global currLines, currRadiuses, currCurves

    for i in range(len(currLines)):
        for j in range(len(currLines[i])):
            currLines[i][j] = newscale * currLines[i][j]

    for i in range(len(currRadiuses)):
        for j in range(len(currRadiuses[i])):
            currRadiuses[i][j] = newscale * currRadiuses[i][j]

    for i in range(len(currCurves)):
        for j in range(len(currCurves[i])):
            currCurves[i][j] = newscale * currCurves[i][j]


    canvas.delete("all")
    drawLines(currLines)
    drawRadiuses(currRadiuses)
    drawCurves(currCurves)

def scaleTranform(newScale, newWindow):
    '''
    Transformation for scaling
    '''
    scaleCanvas(float(newScale.get()))
    newWindow.destroy()

# function to open a new window
# on a button click
def openNewWindow():

    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(window)

    newWindow.title("Enter scale")

    # sets the geometry of toplevel
    newWindow.geometry("400x200")

    # A Label widget to show in toplevel
    Label(newWindow,
          text ="Enter the new scale:").pack()

    newScale = Entry(newWindow)
    newScale.pack()

    #Packing a button to the new window
    Button(newWindow, text="Confirm", command= lambda: scaleTranform(newScale, newWindow),
           height=2, width=10, bg='SkyBlue4', fg='white').pack(side=BOTTOM, pady=15)



def translation_point(tranlation_point,Tx,Ty):
    translationMetrix = [[1,0,0],
                         [0,1,0],
                         [Tx,Ty,1]]
    muMetrix = np.dot([tranlation_point[0],tranlation_point[1],1],translationMetrix)
    return muMetrix


def translationTranform(start, finish):
    clear()
    x = finish[0] - start[0]
    y = finish[1] - start[1]
    global currLines,currRadiuses,currCurves
    for i in currLines:
        result = translation_point([i[0:0], i[0:1]], x, y)
        i[0:0] = result[0]
        i[0:1] = result[1]
        result =  translation_point([i[1][0], i[1][1]], x, y)
        i[1][0] = result[0]
        i[1][1] = result[1]
    for i in currRadiuses:
        result = translation_point([i[0][0], i[0][1]], x, y)
        i[0][0] = result[0]
        i[0][1] = result[1]
        result =  translation_point([i[1][0], i[1][1]], x, y)
        i[1][0] = result[0]
        i[1][1] = result[1]
    for i in currCurves:
        result = translation_point([i[0][0], i[0][1]], x, y)
        i[0][0] = result[0]
        i[0][1] = result[1]
        result =  translation_point([i[1][0], i[1][1]], x, y)
        i[1][0] = result[0]
        i[1][1] = result[1]
        result = translation_point([i[2][0], i[2][1]], x, y)
        i[2][0] = result[0]
        i[2][1] = result[1]
        result =  translation_point([i[3][0], i[3][1]], x, y)
        i[3][0] = result[0]
        i[3][1] = result[1]


def draw():
    global mode
    # if mode == 'trans':
    #     my_translation(points[0], points[1])
    if mode == 'scale':
        openNewWindow()
        # scaleTranform(points[0], points[1])
    # elif mode == 'mirror':
    #     my_mirror()
    # # elif mode == 'shearing':
    #
    # elif mode == 'rotate':
    #     my_rotate(points)


#mouse clicks
canvas.bind("<Button-1>", mouse_click)
canvas.pack()

if __name__ == '__main__':
    # lines , circles, curves = handleFile()
    # print(lines)
    readCoordinates()
    window.mainloop()