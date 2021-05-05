# imports
from tkinter import *
from tkinter import font as tkFont
import math as math
import re
import numpy as np

def clear_data():
    global data
    data = {"lines" : [], "circles": [], "curves": []}
    clear()

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
trans_button = Button(trans_frame, text="Translation", width=16, command=set_trans)
scale_button = Button(trans_frame, text="Scaling big", width=16, command=set_scale)
mirror_button = Button(trans_frame, text="Mirror", width=16, command=set_mirror)
rotate_button = Button(trans_frame, text="Rotate", width=16, command=set_rotate)

#Set in GUI
trans_button.pack( side = "left" )
scale_button.pack( side = "left" )
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



def translationMatrixMultiplier(tranlation_point,Tx,Ty):
    translationMatrix = [[1,0,0],
                         [0,1,0],
                         [Tx,Ty,1]]
    muMatrix = np.dot([tranlation_point[0],tranlation_point[1],1],translationMatrix)
    return muMatrix


def translationTranform(start, finish):
    '''
    This method is creating the linear translation transformation,
    for each element in the painting it multiplies it's values with the translation matrix. 
    '''
    global currLines,currRadiuses,currCurves
    x = finish[0] - start[0]
    y = finish[1] - start[1]


    for i in range(len(currLines)):
        for j in range(len(currLines[i])):
            

    for i in range(len(currRadiuses)):
        for j in range(len(currRadiuses[i])):
            currRadiuses[i][j] = newscale * currRadiuses[i][j]

    for i in range(len(currCurves)):
        for j in range(len(currCurves[i])):















    for i in currLines:
        result = translationMatrixMultiplier([i[0:0], i[0:1]], x, y)
        i[0:0] = result[0]
        i[0:1] = result[1]
        result =  translationMatrixMultiplier([i[1][0], i[1][1]], x, y)
        i[1][0] = result[0]
        i[1][1] = result[1]
    for i in currRadiuses:
        result = translationMatrixMultiplier([i[0][0], i[0][1]], x, y)
        i[0][0] = result[0]
        i[0][1] = result[1]
        result =  translationMatrixMultiplier([i[1][0], i[1][1]], x, y)
        i[1][0] = result[0]
        i[1][1] = result[1]
    for i in currCurves:
        result = translationMatrixMultiplier([i[0][0], i[0][1]], x, y)
        i[0][0] = result[0]
        i[0][1] = result[1]
        result =  translationMatrixMultiplier([i[1][0], i[1][1]], x, y)
        i[1][0] = result[0]
        i[1][1] = result[1]
        result = translationMatrixMultiplier([i[2][0], i[2][1]], x, y)
        i[2][0] = result[0]
        i[2][1] = result[1]
        result =  translationMatrixMultiplier([i[3][0], i[3][1]], x, y)
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



if __name__ == '__main__':
    readCoordinates()
    window.mainloop()