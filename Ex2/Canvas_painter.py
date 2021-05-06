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

def rotatePaintingPoint(rot_point,angle):
    rotateMetrix = [[np.cos(angle),np.sin(angle),0],
                    [(-(np.sin(angle))),np.cos(angle),0],
                    [0,0,1]]
    mulMetrix = np.dot([rot_point[0],rot_point[1],1],rotateMetrix)
    return mulMetrix

def rotatePainting(points,canvas):
    global currLines,currRadiuses,currCurves
    a = np.array(points[0])
    b = np.array(points[1])
    c = np.array(points[2])
    #calculate the angle
    ba = b-a
    ca = c-a

    cosine_angle = np.dot(ba , ca) / (np.linalg.norm(ba) * np.linalg.norm(ca))
    angle = np.arccos(cosine_angle)
    x = list()
    j=0

    # multiply each vector with the matrix
    for i in currLines:
        point = rotatePaintingPoint(i,angle)
        x.insert(j,point)
        j += 1

    for i in range(len(currLines)):
        for j in range(len(currLines[i])):
            currLines[i][j] = point * currLines[i][j]

    for i in range(len(currRadiuses)):
        for j in range(len(currRadiuses[i])):
            currRadiuses[i][j] = point * currRadiuses[i][j]

    for i in range(len(currCurves)):
        for j in range(len(currCurves[i])):
            currCurves[i][j] = point * currCurves[i][j]

    # clear the canvas before painting the new scaled painting
    canvas.delete("all")

    # draw the painting after scaling it to device proportions
    drawLines(currLines, canvas)
    drawRadiuses(currRadiuses, canvas)
    drawCurves(currCurves, canvas)


## Translation

def translation_point(tra_point,Tx,Ty):
    translationMetrix = [[1,0,0],
                         [0,1,0],
                         [Tx,Ty,1]]
    translationMetrix = np.array(translationMetrix)
    muMetrix = np.dot([tra_point[0],tra_point[1],1],translationMetrix)
    return muMetrix

def translationPainting(start,finish,canvas):
    global currLines,currRadiuses,currCurves,mode

    x = finish[0] - start[0]
    y = finish[1] - start[1]

    for i in range(len(currLines)):
         for j in range(len(currLines[i])):

             result = translation_point([currLines[0][0], currLines[0][1]], x, y)
             currLines[0][0] = result[0]
             currLines[0][1] = result[1]
             currLines[0][2] = result[2]
             result =  translation_point([currLines[1][0], currLines[1][1]], x, y)
             currLines[1][0] = result[0]
             currLines[1][1] = result[1]
             currLines[0][2] = result[2]

    for i in range(len(currRadiuses)):
        for j in range(len(currRadiuses[i])):

            result = translation_point([currRadiuses[0][0], currRadiuses[0][1]], x, y)
            currRadiuses[0][0] = result[0]
            currRadiuses[0][1] = result[1]
            currRadiuses[0][2] = result[2]
            result =  translation_point([currRadiuses[1][0], currRadiuses[1][1]], x, y)
            currRadiuses[1][0] = result[0]
            currRadiuses[1][1] = result[1]
            currRadiuses[1][2] = result[2]

    for i in range(len(currCurves)):
        for j in range(len(currCurves[i])):
            result = translation_point([currCurves[0][0], currCurves[0][1]], x, y)
            currCurves[0][0] = result[0]
            currCurves[0][1] = result[1]
            currCurves[0][2] = result[2]
            result =  translation_point([currCurves[1][0], currCurves[1][1]], x, y)
            currCurves[1][0] = result[0]
            currCurves[1][1] = result[1]
            currCurves[1][2] = result[2]
            result = translation_point([currCurves[2][0], currCurves[2][1]], x, y)
            currCurves[2][0] = result[0]
            currCurves[2][1] = result[1]
            currCurves[2][2] = result[2]
            result =  translation_point([currCurves[3][0], currCurves[3][1]], x, y)
            currCurves[3][0] = result[0]
            currCurves[3][1] = result[1]
            currCurves[3][2] = result[2]

# clear the canvas before painting the new scaled painting
    canvas.delete("all")
    mode = "None"
    drawLines(currLines, canvas)
    drawRadiuses(currRadiuses, canvas)
    drawCurves(currCurves, canvas)




