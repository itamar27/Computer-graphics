# Computer Graphics - Exercise 1
# Handling by
# Barak Daniel 204594329, Itamar Yarden 204289987, Sivan Salzmann 207056334

from shapes import *
from fileManager import *

# globals
width = 1080
height = 900
color = '#000000'
window = Tk()
window.geometry('{}x{}'.format(width, height))
window.title('Exercise 2')
window.configure(background='SkyBlue1')
canvas = Canvas(window, width=width-200, height=height, bg="white")

# define font
helv36 = tkFont.Font(family='Helvetica', size=10, weight='bold')

# Functions


def createCoordinates(string):
    '''
    Parse the string from file with the token splitting the arguments
    '''
    string = string[1:-1]
    coor = string.split(',')
    return coor


def drawLines(lines):
    '''
    receive all lines as a list and add them to the canvas
    '''
    for line in lines:
        x1, y1, x2, y2 = createCoordinates(line)
        MyLine(int(x1), int(y1), int(x2), int(y2), canvas)


def drawRadiuses(radiuses):
    '''
    receive all curves as list and add them to the canvas
    '''
    for radius in radiuses:
        x1, y1, r, size = createCoordinates(radius)
        MyCircle(int(x1), int(y1), int(size), canvas)


def drawCurves(curves):
    '''
    receive all curves that are part of the main drawing and add them to the canvas
    '''
    for curve in curves:
        x1, y1, x2, y2, x3, y3, x4, y4 = createCoordinates(curve)
        coordsMatrix = [[int(x1), int(y1)], [int(x2), int(y2)], [
            int(x3), int(y3)], [int(x4), int(y4)]]
        BezierCurve(coordsMatrix, canvas)


def readCoordinates():
    '''
    creating all the coordinates after reading them from file
    '''
    lines, radiuses, curves = selectFile()

    drawLines(lines)
    drawRadiuses(radiuses)
    drawCurves(curves)

def setUpGraphicalEnv():
    '''
    Declaring on all the UI elements and packing them to the canvas
    '''
    # creating UI elements
    fileBtn = Button(window, text="Insert file", command=readCoordinates,
                     height=8, width=50, bg='SkyBlue4', fg='white', font=helv36)

    clearBtn = Button(window, text="Clear Screen", command= lambda: clearCanvas(canvas),
                     height=8, width=50, bg='SkyBlue4', fg='white', font=helv36)

    # packing all window elements
    canvas.pack(side=RIGHT)
    fileBtn.pack(side=TOP)
    clearBtn.pack(side=TOP)

# Main
if __name__ == '__main__':
    setUpGraphicalEnv()
    window.mainloop()
