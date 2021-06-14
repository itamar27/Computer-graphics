import math
from tkinter.constants import TRUE

import mpmath
import numpy as np


class Data:

    def __init__(self, coords, poly_points):
        '''Intiate the main data object '''
        self.coords = coords
        self.poly_points = poly_points
        self.polygons = []

        for poly in self.poly_points:
            tempCords = []
            for point in poly:
                tempCords.append(coords[point])
            
            self.polygons.append(Polygon(tempCords))

        self.sortPolygons()
<<<<<<< Updated upstream
=======
        self.setVisibility()
>>>>>>> Stashed changes

    def sortPolygons(self):
        self.polygons.sort(key=lambda poly: poly.depth, reverse=True)

    def getPolygons(self, type_projection):
        polygons = []
        if type_projection == 'Orthographic':
            for poly in self.polygons:
                polygons.append(poly.orthographicCoords())
        elif type_projection == 'Oblique':
            for poly in self.polygons:
                polygons.append(poly.obliqueCoords())
        elif type_projection == 'Perspective':
            for poly in self.polygons:                
                polygons.append(poly.perspectiveCoords())
        return polygons

    def scale(self, mode):
        newPolygons = []
        for poly in self.polygons:
            poly.scale(mode)
        self.sortPolygons()
        self.setVisibility()

<<<<<<< Updated upstream
=======
    def rotation(self, direction, angle):
        for poly in self.polygons:
            poly.rotation(direction, angle)
        self.sortPolygons()
        self.setVisibility()

    def setVisibility(self):
        ''' 
        Setting the preferred visibilty of each polygon based on it's coords values
        Based on the each polygons "view normal" vector values.
        '''

        xMin, xMax, yMin, yMax, zMin, zMax = tuple(
            self.polygons[0].minMaxValues())

        for poly in self.polygons[1::]:
            values = poly.minMaxValues()
            if values[0] < xMin:
                xMin = values[0]
            if values[1] > xMax:
                xMax = values[1]
            if values[2] < yMin:
                yMin = values[2]
            if values[3] > yMax:
                yMax = values[3]
            if values[4] < zMin:
                zMin = values[4]
            if values[5] > zMax:
                zMax = values[5]

        viewNormal = [(xMax-xMin)/2, (yMax-yMin)/2, (zMax-zMin)/2]

        for poly in self.polygons:
            poly.setVisible(viewNormal)


>>>>>>> Stashed changes
class Polygon:

    def __init__(self, coords):
        '''Intiate polygon object object '''
        self.coords = coords
        self.zIndex = coords[0][2]
        for cord in coords[1:]:
            if cord[2] > self.zIndex:
                self.zIndex = cord[2]
        self.color = 'black'
        self.normal = self.setNormal()
        self.depth = self.minMaxValues()


    def __str__(self):
        return "Coords = {}\nzValues = {}\nColor = {}\nNoraml = {}\n".format(self.coords, self.zIndex, self.color, self.normal)

    def setVisible(self, viewVector):
        '''
        Multiply the polygons vector surface normal with the "view normal" vector
        '''
        self.setNormal()

<<<<<<< Updated upstream
    def surface_normal(self):
        n = [0.0, 0.0, 0.0]
        for i, v_curr in enumerate(self.coords):
            v_next = self.coords[(i+1) % len(self.coords)]
            n[0] += (v_curr[1] - v_next[1]) * (v_curr[2] + v_next[2])
            n[1] += (v_curr[2] - v_next[2]) * (v_curr[0] + v_next[0])
            n[2] += (v_curr[0] - v_next[0]) * (v_curr[1] + v_next[1])

        norm = np.linalg.norm(n)
        if norm==0:
            raise ValueError('zero norm')
        else:
            normalised = n/norm

        normalised_float = [float(np_float) for np_float in normalised]

        return normalised_float
=======
        if(self.normal[2] <= 0):
            self.visible = False
        else:
            self.visible = True

    def setNormal(self):
        '''
        Setting the normal for the polygons surfaces
        '''
        n1 = []
        n2 = []
        if len(self.coords) < 3:
            return

        n1.append(self.coords[1][0] - self.coords[0][0])
        n1.append(self.coords[1][1] - self.coords[0][1])
        # n1.append(self.coords[1][2] - self.coords[0][2])
        n1.append(0)
        n2.append(self.coords[2][0] - self.coords[1][0])
        n2.append(self.coords[2][1] - self.coords[1][1])
        # n2.append(self.coords[2][2] - self.coords[1][2])
        n2.append(0)
        normal = [0, 0, 0]
        normal[0] = n1[1]*n2[2] - n1[2]*n2[1]
        normal[1] = n1[2]*n2[0] - n1[0]*n2[2]
        normal[2] = n1[0]*n2[1] - n1[1]*n2[0]

        self.normal = normal
>>>>>>> Stashed changes

    def orthographicCoords(self):
        ''' Return orthographic coordinates for 3d projects (for each polygon)'''
        coordsOrthographic = []

        # Create the orthographic matrix
        ortographicMatrix = [[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 1]]

        for point in self.coords:
            new_point = [point[0], point[1], point[2], 1]
            coords = np.matmul(new_point, ortographicMatrix)
            coordsOrthographic.append((coords[0], coords[1]))
        return coordsOrthographic

    def obliqueCoords(self):
        ''' Return oblique coordinates for 3d projects (for each polygon)'''
        coordsOblique = []
        v1 = -0.5 * math.cos(30 * math.pi / 180)
        v2 = -0.5 * math.sin(30 * math.pi / 180)

        # create the oblique coords matrix
        obliqueMatrix = [[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [v1, v2, 1, 0],
                         [0, 0, 0, 1]]

        for point in self.coords:
            new_point = [point[0], point[1], point[2], 1]
            coords = np.matmul(new_point, obliqueMatrix)
            coordsOblique.append((coords[0], coords[1]))

        return coordsOblique

    def perspectiveCoords(self):
        ''' Return perspective coordinates for 3d projects (for each polygon), where the distance is set to 350'''
        coordsPerspective = []
        # Setting the distance variable
        D = 500

        for point in self.coords:
            sz = D / (int(point[2]) + D)
            # create the perspective coords matrix
            perspectiveMatrix = np.array([[sz, 0, 0, 0],
                                          [0, sz, 0, 0],
                                          [0, 0, 0, 0],
                                          [0, 0, 0, 1]])

<<<<<<< Updated upstream
            new_point = [int(point[0]),int(point[1]),int(point[2]),1]
            coords = np.matmul(new_point, perspectiveMatrix)
            coordsPerspective.append((int(coords[0]),int(coords[1])))
=======
            new_point = [float(point[0]), float(point[1]), float(point[2]), 1]
            coords = np.matmul(new_point, perspectiveMatrix)
            coordsPerspective.append((float(coords[0]), float(coords[1])))
>>>>>>> Stashed changes
        return coordsPerspective

    def minMaxValues(self):
        '''minMaxes will be filled with: [min x, max x, min y, max y, min z, max z]'''
        minMaxes = []
        xVals = []
        yVals = []
        zVals = []

        for cord in self.coords:
            xVals.append(cord[0])
            yVals.append(cord[1])
            zVals.append(cord[2])

        minMaxes.append(min(xVals))
        minMaxes.append(max(xVals))
        minMaxes.append(min(yVals))
        minMaxes.append(max(yVals))
        minMaxes.append(min(zVals))
        minMaxes.append(max(zVals))

        return minMaxes

    def scale(self, mode):
       
        Sx = Sy = Sz = -1

        # choose which scaling transformation to do
        if mode == "out":
            Sx = Sy = Sz = 0.9
        elif mode == "in":
            Sx = Sy = Sz = 1.1

        mulMatrix = np.array(
            [[Sx, 0, 0, 0],
             [0, Sy, 0, 0],
             [0, 0, Sz, 0],
             [0, 0, 0, 1]]
        )
        coords = []

        for coord in self.coords:
<<<<<<< Updated upstream
            new_point = [int(coord[0]),int(coord[1]),int(coord[2]),1]
            tmp = np.matmul(new_point, mulMatrix)
            tmp = [int(x) for x in tmp]
            tmp =tmp[:-1]
=======
            new_point = [float(coord[0]), float(coord[1]), float(coord[2]), 1]
            tmp = np.matmul(new_point, mulMatrix)
            tmp = [float(x) for x in tmp]
            tmp = tmp[:-1]
            coords.append(tmp)
        self.coords = coords

    def rotation(self, direction, angle):
        mulMatrix = []
        cos_angle = math.cos(angle * math.pi / 180)
        sin_angle = math.sin(angle * math.pi / 180)

        if direction == 'x':
            mulMatrix = ([
                [1, 0, 0, 0],
                [0, cos_angle, sin_angle, 0],
                [0, -sin_angle, cos_angle, 0],
                [0, 0, 0, 1]
            ])
        elif direction == 'y':
            mulMatrix = ([
                [cos_angle, 0, -sin_angle,  0],
                [0,         1, 0,           0],
                [sin_angle, 0, cos_angle,   0],
                [0,         0, 0,           1]
            ])
        elif direction == 'z':
            mulMatrix = ([
                [cos_angle, sin_angle, 0, 0],
                [-sin_angle, cos_angle, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
        coords = []
        for coord in self.coords:
            new_point = [float(coord[0]), float(coord[1]), float(coord[2]), 1]
            tmp = np.matmul(new_point, mulMatrix)
            tmp = [float(x) for x in tmp]
            tmp = tmp[:-1]
>>>>>>> Stashed changes
            coords.append(tmp)
        self.coords = coords
