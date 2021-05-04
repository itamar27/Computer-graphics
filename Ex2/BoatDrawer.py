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

def scaleInputToScreen(lines, radiuses, curves):
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
        if(max(int(x1),int(x2)) > maxWidth):
            maxWidth = max(int(x1),int(x2))
        if(max(int(y1),int(y2)) > maxHeight):
            maxHeight = max(int(y1),int(y2))
        
    for radius in radiuses:
        x1, y1, r, size = createCoordinates(radius)
        if(int(x1)+int(size) > maxWidth):
            maxWidth = int(x1)+int(size)
        if(int(y1)+int(size) > maxHeight):
            maxHeight = int(y1)+int(size)

    for curve in curves:
        x1, y1, x2, y2, x3, y3, x4, y4 = createCoordinates(curve)
        if(max(int(x1),int(x2), int(x3), int(x4)) > maxWidth):
            maxWidth = max(int(x1),int(x2), int(x3), int(x4))
        if(max(int(y1),int(y2), int(y3),int(y4)) > maxHeight):
            maxHeight = max(int(y1),int(y2), int(y3),int(y4))
    
    newLines = []
    newRadiuses = []
    newCurves = []

    # Normalizing the vectors by dividing them with the width/height of the max values found in the vectors, 
    # then scaling them by multiplying with the actual window width/height. (width-200 is regarding to the part of the window we paint on)

    for line in lines:
        x1, y1, x2, y2 = createCoordinates(line)
        newLines.append([int(x1)/maxWidth*(width-200), int(y1)/maxHeight*height, int(x2)/maxWidth*(width-200), int(y2)/maxHeight*height])

    for radius in radiuses:
         x1, y1, r, size = createCoordinates(radius)
         newRadiuses.append([int(x1)/maxWidth*(width-200), int(y1)/maxHeight*height, int(size)/((maxHeight+maxWidth)/2)*((height+(width-200))/2)])
    
    for curve in curves:
        x1, y1, x2, y2, x3, y3, x4, y4 = createCoordinates(curve)
        newCurves.append([int(x1)/maxWidth*(width-200), int(y1)/maxHeight*height, int(x2)/maxWidth*(width-200), int(y2)/maxHeight*height, int(x3)/maxWidth*(width-200), int(y3)/maxHeight*height, int(x4)/maxWidth*(width-200), int(y4)/maxHeight*height])
        
    return newLines, newRadiuses, newCurves

def drawLines(lines):
    '''
    receive all lines as a list and add them to the canvas
    '''
    for line in lines:
        x1, y1, x2, y2 = line
        MyLine(int(x1), int(y1), int(x2), int(y2), canvas)


def drawRadiuses(radiuses):
    '''
    receive all curves as list and add them to the canvas
    '''
    for radius in radiuses:
        x1, y1, size = radius
        MyCircle(int(x1), int(y1), int(size), canvas)


def drawCurves(curves):
    '''
    receive all curves that are part of the main drawing and add them to the canvas
    '''
    for curve in curves:
        x1, y1, x2, y2, x3, y3, x4, y4 = curve
        coordsMatrix = [[int(x1), int(y1)], [int(x2), int(y2)], [
            int(x3), int(y3)], [int(x4), int(y4)]]
        BezierCurve(coordsMatrix, canvas)


def readCoordinates():
    '''
    Getting Cordinates from the file input,
    then scaling the vectors to our window size,
    then painting the data to the window.
    '''
    lines, radiuses, curves = selectFile()

    lines, radiuses, curves = scaleInputToScreen(lines, radiuses, curves)

    drawLines(lines)
    drawRadiuses(radiuses)
    drawCurves(curves)

# function to open a new window 
# on a button click
def openNewWindow():
      
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(window)
  
    newWindow.title("Enter params")
  
    # sets the geometry of toplevel
    newWindow.geometry("400x200")
  
    # A Label widget to show in toplevel
    Label(newWindow, 
          text ="Enter params:").pack()

    confirmBtn = Button(newWindow, text="Confirm", command=lambda: print("Confirm"),
                     height=2, width=10, bg='SkyBlue4', fg='white', font=helv36).pack(side=BOTTOM, pady=15)


def setUpGraphicalEnv():
    '''
    Declaring on all the UI elements and packing them to the canvas
    '''
    # creating UI elements
    fileBtn = Button(window, text="Insert file", command=readCoordinates,
                     height=8, width=50, bg='SkyBlue4', fg='white', font=helv36)
    translateBtn = Button(window, text="Translate painting", command=openNewWindow,
                     height=8, width=50, bg='SkyBlue4', fg='white', font=helv36)
    scaleBtn = Button(window, text="Scale painting", command= lambda: print("scale command"),
                     height=8, width=50, bg='SkyBlue4', fg='white', font=helv36)
    rotateBtn = Button(window, text="Rotate painting", command= lambda: print("rotate command"),
                     height=8, width=50, bg='SkyBlue4', fg='white', font=helv36)
    reflectBtn = Button(window, text="Reflect painting", command= lambda: print("reflect command"),
                     height=8, width=50, bg='SkyBlue4', fg='white', font=helv36)
    shearBtn = Button(window, text="Shearing painting", command= lambda: print("shear command"),
                     height=8, width=50, bg='SkyBlue4', fg='white', font=helv36)
    clearBtn = Button(window, text="Clear Screen", command= lambda: clearCanvas(canvas),
                     height=8, width=50, bg='SkyBlue4', fg='white', font=helv36)

    # packing all window elements
    canvas.pack(side=RIGHT)
    fileBtn.pack(side=TOP)
    translateBtn.pack(side=TOP) 
    scaleBtn.pack(side=TOP)   
    rotateBtn.pack(side=TOP)
    reflectBtn.pack(side=TOP)
    shearBtn.pack(side=TOP)
    clearBtn.pack(side=TOP)

# Main
if __name__ == '__main__':
    setUpGraphicalEnv()
    window.mainloop()
