from tkinter import StringVar
from tkinter.filedialog import askopenfilename

class FileManager():

    def openFile(self):
        '''
        Open the files explorer and let you choose the descriptive file
        '''
        folder_path = StringVar()
        filename = askopenfilename()
        folder_path.set(filename)
        return self.readFile(filename)

    def  readFile(self, name):
        '''
        Read file data inorder to get the coordinate and polygons location on  screen
        '''
        category = ""
        coords = []
        polygons = []
        with open(name) as f:
            fileLines = f.read().splitlines()                      
            for line in fileLines:
                line = line.split(" ")
                if line[0] == "#coords":
                    category = "coords"
                elif line[0] == "#polygons":
                    category = "polygon"
                
                elif category == "coords":
                    if len(line) > 1:
                        coor = line[1].split(",")
                        coords.append([int(x) for x in coor])
                elif category == "polygon":
                    if len(line) > 1:
                        poly = line[1].split(",")
                        polygons.append([int(x)-1 for x in poly])

        return coords, polygons
        