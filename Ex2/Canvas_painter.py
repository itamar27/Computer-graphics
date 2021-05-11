# imports
from tkinter import *
from tkinter import font as tkFont
from fileManager import *
import math as math
import re
import numpy as np

# Globals
currLines = []
currRadiuses = []
currCurves = []
xMax = 0
yMax = 0



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



### Addition part for 2D transformations

def drawLines(lines, canvas):
    '''
    receive all lines as a list and add them to the canvas
    '''
    for line in lines:
        x1, y1, x2, y2 = line
        MyLine(int(x1), int(y1), int(x2), int(y2), canvas)


def drawRadiuses(radiuses, canvas):
    '''
    receive all curves as list and add them to the canvas
    '''
    for radius in radiuses:
        x1, y1, size = radius
        MyCircle(int(x1), int(y1), int(size), canvas)


def drawCurves(curves,canvas):
    '''
    receive all curves that are part of the main drawing and add them to the canvas
    '''
    for curve in curves:
        x1, y1, x2, y2, x3, y3, x4, y4 = curve
        coordsMatrix = [[int(x1), int(y1)], [int(x2), int(y2)], [
            int(x3), int(y3)], [int(x4), int(y4)]]
        BezierCurve(coordsMatrix, canvas)


def readCoordinates(width, height, canvas):
    '''
    Getting Coordinates from the file input,
    then scaling the vectors to our window size,
    then painting the data to the window.
    '''

    # read from file the graphical elements
    lines, radiuses, curves = selectFile()

    # scale the world coordinates into device coordinates
    lines, radiuses, curves = scaleInputToScreen(lines, radiuses, curves, width, height)

    #
    drawLines(lines, canvas)
    drawRadiuses(radiuses, canvas)
    drawCurves(curves,canvas)


def scaleInputToScreen(lines, radiuses, curves, width, height):
    '''
    Getting a vector representation of a painting, then scales it to the actual board size.
    The method is to normalize the vectors and then scale them to the actual window size, for that
    we are finding the maxHeight/maxWidth of the painting in the input vectors and using the actual window
    width and height to scale.
    '''
    maxWidth = 0
    maxHeight = 0


    for line in lines:
        x1, y1, x2, y2 = createCoordinates(line)
        if(max(int(x1), int(x2)) > maxWidth):
            maxWidth = max(int(x1), int(x2))
        if(max(int(y1), int(y2)) > maxHeight):
            maxHeight = max(int(y1), int(y2))

    for radius in radiuses:
        x1, y1, r, size = createCoordinates(radius)
        if(int(x1)+int(size) > maxWidth):
            maxWidth = int(x1)+int(size)
        if(int(y1)+int(size) > maxHeight):
            maxHeight = int(y1)+int(size)

    for curve in curves:
        x1, y1, x2, y2, x3, y3, x4, y4 = createCoordinates(curve)
        if(max(int(x1), int(x2), int(x3), int(x4)) > maxWidth):
            maxWidth = max(int(x1), int(x2), int(x3), int(x4))
        if(max(int(y1), int(y2), int(y3), int(y4)) > maxHeight):
            maxHeight = max(int(y1), int(y2), int(y3), int(y4))

    newLines = []
    newRadiuses = []
    newCurves = []

    # Normalizing the vectors by dividing them with the width/height of the max values found in the vectors,
    # then scaling them by multiplying with the actual window width/height.

    for line in lines:
        x1, y1, x2, y2 = createCoordinates(line)
        newLines.append([int(x1)/maxWidth*(width), int(y1)/maxHeight *
                        height, int(x2)/maxWidth*(width), int(y2)/maxHeight*height])

    for radius in radiuses:
        x1, y1, r, size = createCoordinates(radius)
        newRadiuses.append([int(x1)/maxWidth*(width), int(y1)/maxHeight *
                           height, int(size)/((maxHeight+maxWidth)/2)*((height+(width))/2)])

    for curve in curves:
        x1, y1, x2, y2, x3, y3, x4, y4 = createCoordinates(curve)
        newCurves.append([int(x1)/maxWidth*(width), int(y1)/maxHeight*height, int(x2)/maxWidth*(width), int(y2)/maxHeight *
                         height, int(x3)/maxWidth*(width), int(y3)/maxHeight*height, int(x4)/maxWidth*(width), int(y4)/maxHeight*height])

    global xMax, yMax, currLines, currRadiuses, currCurves
    xMax = maxWidth
    yMax = maxHeight

    newLines = np.array(newLines)
    newLines = newLines.astype(int)
    currLines = newLines

    newRadiuses = np.array(newRadiuses)
    newRadiuses = newRadiuses.astype(int)
    currRadiuses = newRadiuses

    newCurves = np.array(newCurves)
    newCurves = newCurves.astype(int)
    currCurves = newCurves

    return newLines, newRadiuses, newCurves

def createCoordinates(string):
    '''
    Parse the string from file with the token splitting the arguments
    '''
    string = string[1:-1]
    coor = string.split(',')
    return coor



### Linear Transformation implementation
#initilize drawing
def init_draw():
    global point_index
    point_index = 0

def scalePainting(canvas, newscale=0.5):
    '''
    Scales the canvas painting by a given scale, default is 0.5
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

    # clear the canvas before painting the new scaled painting
    canvas.delete("all")

    # draw the painting after scaling it to device proportions
    drawLines(currLines, canvas)
    drawRadiuses(currRadiuses, canvas)
    drawCurves(currCurves, canvas)


def mirrorPainting():
    print("hello world")

### Rotation

def makeDagree(points):
    a = np.array(points[0])
    b = np.array(points[1])
    c = np.array(points[2])

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return angle

def rotatePainting(points,canvas):
    global currLines,currRadiuses,currCurves,xMax, yMax
    print(xMax,yMax)
    # clear the canvas before painting the new scaled painting
    canvas.delete("all")

    angle = makeDagree(points)
    print(angle)

    # set sinus and cosinus
    sinus = math.sin(20 / 180 * math.pi)
    cosinus = math.cos(20 / 180 * math.pi)

    # intalize 3 new lists to put in them the new coordinates
    newLines = []
    newCurves = []
    newCircles = []

    # transform lines
    for line in currLines:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]

        # new lines
        newLines.append([x1 * cosinus - y1 * sinus, y1 * cosinus + x1 * sinus, x2 * cosinus - y2 * sinus, y2 * cosinus + x2 * sinus])

    # transform curves
    for curve in currCurves:
        x1 = curve[0]
        y1 = curve[1]
        x2 = curve[2]
        y2 = curve[3]
        x3 = curve[4]
        y3 = curve[5]
        x4 = curve[6]
        y4 = curve[7]

        # new curves
        newCurves.append([
            x1 * cosinus - y1 * sinus,
            x1 * sinus + y1 * cosinus,
            x2 * cosinus - y2 * sinus,
            x2 * sinus + y2 * cosinus,
            x3 * cosinus - y3 * sinus,
            x3 * sinus + y3 * cosinus,
            x4 * cosinus - y4 * sinus,
            x4 * sinus + y4 * cosinus
        ])

    # transform circles
    for circle in currRadiuses:
        x = circle[0]
        y = circle[1]

        # new circles
        newCircles.append([x * cosinus - y * sinus, x * sinus + y * cosinus, circle[2]])

    # draw the painting after scaling it to device proportions
    drawLines(newLines, canvas)
    drawRadiuses(newCircles, canvas)
    drawCurves(newCurves, canvas)


## Translation

def translationPainting(Tx, Ty, canvas):
    global currLines,currRadiuses,currCurves

    # clear the canvas before painting the new scaled painting
    canvas.delete("all")

    newLines = []
    newCircles = []
    newCurves = []

    for line in currLines:
        newLines.append([line[0] + Tx, line[1] + Ty, line[2] + Tx, line[3] + Ty])

    for circle in currRadiuses:
        newCircles.append([circle[0] + Tx, circle[1] + Ty, circle[2]])

    for curve in currCurves:
        tmpCurves = []
        for i,curr in enumerate(curve):
            tmpCurves.append(Tx + curr if i % 2 == 0 else curr + Ty)
        newCurves.append(tmpCurves)

    drawLines(newLines, canvas)
    drawRadiuses(newCircles, canvas)
    drawCurves(newCurves, canvas)




