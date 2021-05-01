# imports
from tkinter import *
from tkinter import font as tkFont
import math as math
import re


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
