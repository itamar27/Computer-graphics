# from tkinter import *
# from tkinter import font as tkFont 


# # Globals
# width = 1000
# height = 500
# x = 10
# y = 10


# # creating a main screen with title
# root = Tk()
# root.title('Exercise_1')

# # define font
# helv36 = tkFont.Font(family='Helvetica', size=10, weight='bold')

# # creating a button widget and shoving it to the screen
# lineButton = Button(root, text='Line' ,bg ='RoyalBlue4', fg ='white')
# lineButton['font'] =  helv36

# lineButton.grid(row=0, column=0)

# circleButton = Button(root, text='Circle')
# circleButton.grid(row=0, column=1)

# curveButton = Button(root, text='Curve')
# curveButton.grid(row=0, column=2)

# # creating canvas and shoving it to the screen
# canvas = Canvas(root, width=width, height=height, bg="black")
# img = PhotoImage()
# canvas.create_image((width // 2, height // 2), image=img, state="normal")
# canvas.grid()

# #setup UI

# # paint pixel

# # paint line

# # paint circle

# root.mainloop()

num = 6.6
num1 = round(num)
num2 = int(num)

print(num1, num2)
