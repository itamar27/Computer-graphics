# Computer Graphics - Exercise 1
# Handling by
# Barak Daniel 204594329, Itamar Yarden 204289987

from tkinter import *
from tkinter import font as tkFont
import math as math
import re

# classes


class ClicksManager:
    '''
    This class will help to control the software functions
    and also to manage the click events happening on the main canvas board.
    '''
    counter = 0
    maxCount = 0
    clicks = []
    toDraw = ''

    def draw(self):
        '''
        Class method to go between the main drawing functions that are provided by the software
        '''
        if self.toDraw == 'line':
            MyLine(self.clicks[0][0], self.clicks[0][1],
                   self.clicks[1][0], self.clicks[1][1])
        elif self.toDraw == 'circle':
            MyCircle(self.clicks[0][0], self.clicks[0][1],
                     self.clicks[1][0], self.clicks[1][1])
        elif self.toDraw == 'curve':
            bezierCurve(self.clicks)

        self.counter = 0
        self.clicks = []

    def drawLine(self):
        '''
        Choose draw line function after clicking GUI "line" button
        '''
        self.toDraw = 'line'
        self.counter = 0
        self.maxCount = 2
        self.clicks = []

    def drawCircle(self):
        '''
        Choose draw circle function after clicking GUI "circle" button
        '''
        self.toDraw = 'circle'
        self.counter = 0
        self.maxCount = 2
        self.clicks = []

    def drawCurve(self):
        '''
        Choose draw curve function after clicking GUI "curve" button
        '''
        self.toDraw = 'curve'
        self.counter = 0
        self.maxCount = 4
        self.clicks = []


# globals
width = 1000
height = 700
color = '#000000'
window = Tk()
window.geometry('{}x{}'.format(width, height))
window.title('Exercise 1')
window.configure(background='RoyalBlue1')
canvas = Canvas(window, width=width-200, height=height, bg="white")
clicksManager = ClicksManager()


# define font
helv36 = tkFont.Font(family='Helvetica', size=10, weight='bold')


# functions
def clearCanvas():
    global canvas
    canvas.delete("all")


def drawPixel(x, y):
    '''
    Draw one pixel on the canvas bored that the function received as an argument
    Because tkinter doesn't have any function like 'PutPixel()', we will use a manipulation on the create_rectangle methods
    '''
    global canvas, colorInput
    colorString = "#" + colorInput.get()
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', colorString)
    if(match):
        canvas.create_line(x, y, x + 1, y)
        #canvas.create_rectangle((x, y) * 2, outline=colorString)


def MyLine(x0, y0, x1, y1):
    '''
    DDA implementation for drawing a line between 2 given points, (x0, y0) and (x1, y1).
    '''
    global canvas
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
        drawPixel(round(x), round(y))
        oldY = y
        oldX = x
        x = x + deltaX
        y = y + deltaY

        # smoothening the line draw with more pixels when we step on the shorter axis
        if x_longer:
            if round(oldY) != round(y):
                drawPixel(round(oldX), round(y))
        else:
            if round(oldX) != round(x):
                drawPixel(round(x), round(oldY))


def drawCircle(xc, yc, x, y):
    '''
    Help function for the MyCircle() draw operation, draws a pixel for every
    1/8 of the circles outline (radius)
    '''
    drawPixel(xc+x, yc+y)
    drawPixel(xc-x, yc+y)
    drawPixel(xc+x, yc-y)
    drawPixel(xc-x, yc-y)
    drawPixel(xc+y, yc+x)
    drawPixel(xc-y, yc+x)
    drawPixel(xc+y, yc-x)
    drawPixel(xc-y, yc-x)


def MyCircle(x0, y0, x1, y1):
    '''
    This function is drawing a circle with bezier circle algorithm,
    dividing the circle to 8 parts, that way it is more efficient. 
    '''
    radius = int(math.sqrt(abs(x1-x0)**2+abs(y1-y0)**2))
    x = 0
    y = radius
    p = 3 - 2*radius

    while(y >= x):

        if(p > 0):
            y -= 1
            p = p + 4 * (x - y) + 10
        else:
            p = p + 4 * x + 6
        drawCircle(x0, y0, x, y)
        x += 1


def bezierCurve(coordsMatrix):
    '''
    This function is drawing the Bezier curve, choosing 4 control points
    the curve must go through the two nodes and hold its place with the other points. 
    '''
    global linesInput
    # deciding the curve break down to lines according to user's input
    numOfLines = int(linesInput.get())

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
        MyLine(x0, y0, x1, y1)
        x0, y0 = x1, y1
        t = t + deltaT


def click(event):
    '''
    This function capture the coordinates of a mouse click and stores them.
    '''
    global clicksManager
    if clicksManager.counter < clicksManager.maxCount:
        clicksManager.clicks.append([event.x, event.y])
        clicksManager.counter += 1
    if clicksManager.counter == clicksManager.maxCount:
        clicksManager.draw()


# setting up the graphical environment
canvas.bind('<Button-1>', click)
lineBtn = Button(window, text="Line", command=clicksManager.drawLine,
                 height=8, width=25, bg='RoyalBlue4', fg='white')
lineBtn['font'] = helv36
circleBtn = Button(window, text="Circle", command=clicksManager.drawCircle,
                   height=8, width=25, bg='RoyalBlue4', fg='white')
circleBtn['font'] = helv36
curveBtn = Button(window, text="Curve", command=clicksManager.drawCurve,
                  height=8, width=25, bg='RoyalBlue4', fg='white')
curveBtn['font'] = helv36
clearBtn = Button(window, text="Clear", command=clearCanvas,
                  height=8, width=25, bg='RoyalBlue4', fg='white')
clearBtn['font'] = helv36
colorLabel = Label(window, bg='RoyalBlue1', fg='white',
                   text="Enter color (HEX)")
colorLabel['font'] = helv36
colorInput = Entry(window)
colorInput.insert(END, '000000')
linesLabel = Label(window, bg='RoyalBlue1', fg='white', text="Number of lines")
linesLabel['font'] = helv36
linesInput = Entry(window)
linesInput.insert(END, '20')


# Packing up the graphical environment
canvas.pack(side=RIGHT)
lineBtn.pack(side=TOP)
circleBtn.pack(side=TOP)
curveBtn.pack(side=TOP)
clearBtn.pack(side=TOP)
colorLabel.pack(side=TOP, pady=10)
colorInput.pack(side=TOP)
linesLabel.pack(side=TOP, pady=10)
linesInput.pack(side=TOP)


# Running the application
window.mainloop()
