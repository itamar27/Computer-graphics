import math
from tkinter.constants import TRUE

import mpmath
import numpy as np

class Data:
    
    def __init__(self, coords, poly_points):
        self.coords = coords
        self.poly_points = poly_points
        self.polygons = []

        for poly in self.poly_points:
            tempCords = []
            for point in poly:
                tempCords.append(coords[point])
            
            self.polygons.append(Polygon(tempCords))

        self.sortPolygons()

    def sortPolygons(self):
        self.polygons.sort(key=lambda poly: poly.depth, reverse=True)

        for poly in self.polygons:
            print(poly.coords)         
        
        

    def getPolygons(self,type_projection):
        polygons = []
        if type_projection == 'Orthographic':
            for poly in self.polygons:
                polygons.append(poly.orthographicCoords())
        if type_projection == 'Oblique':
            for poly in self.polygons:
                polygons.append(poly.obliqueCoords())
        if type_projection == 'Perspective':
            for poly in self.polygons:
                polygons.append(poly.perspectiveCoords())
        return polygons

        

class Polygon:
    def __init__(self, coords):
        self.coords = coords
        self.zIndex = coords[0][2]
        for cord in coords[1:]:
            if cord[2] > self.zIndex:
                self.zIndex = cord[2]
        self.color = 'black'
        self.normal = self.surface_normal()
        self.depth = self.minMaxValues()


    def __str__(self):
        return "Coords = {}\nzValues = {}\nColor = {}\nNoraml = {}\n".format(self.coords, self.zIndex, self.color,self.normal)

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

    def orthographicCoords(self):
        coordsOrthographic = []
        ortographicMatrix = [[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 1]]

        for point in self.coords:
            new_point = [point[0],point[1],point[2],1]
            coords = np.matmul(new_point, ortographicMatrix)
            coordsOrthographic.append((coords[0],coords[1]))

        return coordsOrthographic

    def obliqueCoords(self):
        coordsOblique = []
        v1 = 0.5 * math.cos(30 * math.pi / 180)
        v2 = 0.5 * math.sin(30 * math.pi / 180)
        obliqueMatrix = [[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [v1, v2, 1, 0],
                          [0, 0, 0, 1]]

        for point in self.coords:
            new_point = [point[0],point[1],point[2],1]
            coords = np.matmul(new_point, obliqueMatrix)
            coordsOblique.append((coords[0],coords[1]))

        return coordsOblique

    def perspectiveCoords(self):
        coordsPerspective = []
        D = 350

        for point in self.coords:
            sz = D / (point[2] + D)
            perspectiveMatrix = [[sz, 0, 0, 0],
                                 [0, sz, 0, 0],
                                 [0, 0, 0, 0],
                                 [0, 0, 0, 1]]
            new_point = [point[0],point[1],point[2],1]
            coords = np.matmul(new_point, perspectiveMatrix)
            coordsPerspective.append((coords[0],coords[1]))

        return coordsPerspective

    def minMaxValues(self):
        
        # minMaxes will be filled with: [min x, max x, min y, max y, min z, max z]
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

