# Handling by
# Barak Daniel 204594329
# Itamar Yarden 204289987

from tkinter import *
import math as math

# globals
window = Tk()
window.geometry('800x600')
window.title('Exercise 1')
width = 800
height = 600
click1 = {"x": -1, "y": -1}
click2 = {"x": -1, "y": -1}
counter = 0
canvas = Canvas(window, width=width, height=height, bg="white")


# functions


def drawPixel(x, y, color):
    '''
    Draw one pixel on the canvas bored that the function received as an argument
    Because tkinter doesn't have any function like 'PutPixel()', we will use a manipulation on the create_rectangle methos
    '''
    global canvas
    canvas.create_rectangle((x, y) * 2, outline=color)


def DDA(x0, y0, x1, y1):
    '''
    COMMENT LATER!!!!!!!!!!!!!!!!!!!!!!!
    '''
    global canvas, counter
    myRange = max(abs(x1-x0), abs(y1-y0))

    deltaX = (x1-x0)/myRange
    deltaY = (y1-y0)/myRange
    x = x0
    y = y0

    for move in range(0, myRange):
         drawPixel(round(x), round(y), 'black')
         x = x + deltaX
         y = y + deltaY
    counter = 0


def click(event):
    '''
    This function capture 
    '''
    global click1, click2, counter
    if counter == 0:
        click1['x'], click1['y'] = event.x, event.y
        counter += 1
    elif counter == 1:
        click2['x'], click2['y'] = event.x, event.y
        DDA(click1['x'], click1['y'], click2['x'], click2['y'])


# setting up the graphical environment
window.bind('<Button-1>', click)

canvas.pack()

print(100 // 2)

# #running the application
window.mainloop()
