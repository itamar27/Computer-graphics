###
# Students name:
# Sivan Salzmann - 207056334
# Barak Daniel - 204594329
# Itamer Yarden - 204289987
###
import math
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
        self.setVisiblity()

    def sortPolygons(self):
        '''Sort the polgons by Zindex and make reverse'''
        for poly in self.polygons:
            poly.setZIndex()
            
        self.polygons.sort(key=lambda poly: poly.zIndex, reverse=True)



    def getPolygons(self,type_projection):
        '''Get all the polygons and append them to specific projection
        that get from the type_projection variable '''
        polygons = []
        self.sortPolygons()
        if type_projection == 'Orthographic':
            for poly in self.polygons:
                if poly.visible:
                    polygons.append(poly.orthographicCoords())
        elif type_projection == 'Oblique':
            for poly in self.polygons:
                # if poly.visible:
                    polygons.append(poly.obliqueCoords())
        elif type_projection == 'Perspective':
            for poly in self.polygons:
                if poly.visible:
                    polygons.append(poly.perspectiveCoords())
        return polygons
    
    def scale(self, mode):
        '''Scale transform'''
        for poly in self.polygons:
            poly.scale(mode)

    def rotation(self,direction,angle):
        '''Rotation transform'''
        for poly in self.polygons:
            poly.rotation(direction,angle)
        self.sortPolygons()
        self.setVisiblity()

    def setVisiblity(self):
        for poly in self.polygons:
            poly.setVisible()


class Polygon:

    def __init__(self, coords):
        '''Intiate polygon object object '''
        self.coords = coords
        self.zIndex = coords[0][2]
        for cord in coords[1:]:
            if cord[2] > self.zIndex:
                self.zIndex = cord[2]
        self.color = 'black'
        self.normal = self.surface_normal()
        self.depth = self.minMaxValues()
        self.visible = False

    def setZIndex(self):
        ''' This function change the z index of polygon to
            the max value between all the z value in'''
        self.zIndex = self.coords[0][2]
        for cord in self.coords[1:]:
            if cord[2] > self.zIndex:
                self.zIndex = cord[2]


    def setVisible(self):
        ''' Check if vis <= 0 the visible is invisible,
        and the opposite if vis > 0 '''
        self.surface_normal()
        viewVector = [0,0,-1000]
        tmp = np.subtract(self.coords[0], viewVector)
        vis = np.dot(tmp, self.normal)
        if(vis <= 0):
            self.visible = False
        else:
            self.visible = True

    def surface_normal(self):
        '''Calculate the normal'''
        n1 = []
        n2 = []
        if len(self.coords) < 3:
            return

        n1.append(self.coords[1][0] - self.coords[0][0])
        n1.append(self.coords[1][1] - self.coords[0][1])
        n1.append(self.coords[1][2] - self.coords[0][2])

        n2.append(self.coords[2][0] - self.coords[1][0])
        n2.append(self.coords[2][1] - self.coords[1][1])
        n2.append(self.coords[2][2] - self.coords[1][2])

        self.normal = np.cross(n1,n2)

    def orthographicCoords(self):
        ''' Return orthographic coordinates for 3d projects (for each polygon)'''
        coordsOrthographic = []

        # Create the orthographic matrix
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
        ''' Return oblique coordinates for 3d projects (for each polygon)'''
        coordsOblique = []
        v1 = 0.5 * math.cos(30 * math.pi / 180)
        v2 = 0.5 * math.sin(30 * math.pi / 180)

        #create the oblique coords matrix
        obliqueMatrix = np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [v1, v2, 1, 0],
                          [0, 0, 0, 1]])

        for point in self.coords:
            new_point = [float(point[0]),float(point[1]),float(point[2]),1]
            coords = np.matmul(new_point, obliqueMatrix)
            coordsOblique.append((float(coords[0]),float(coords[1])))
        return coordsOblique

    def perspectiveCoords(self):
        ''' Return perspective coordinates for 3d projects (for each polygon), where the distance is set to 350'''
        coordsPerspective = []
        #Setting the distance variable
        D = 1000

        for point in self.coords:
            sz = D / (int(point[2]) + D)
            #create the perspective coords matrix 
            perspectiveMatrix = np.array([[sz, 0, 0, 0],
                                 [0, sz, 0, 0],
                                 [0, 0, 0, 0],
                                 [0, 0, 0, 1]])

            new_point = [float(point[0]),float(point[1]),float(point[2]),1]
            coords = np.matmul(new_point, perspectiveMatrix)
            coordsPerspective.append((float(coords[0]),float(coords[1])))
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
        ''' Scale transformation multiplier every value
        with the mulMatrix and change: Sx,Sy,Sz by the
        wanted transformation: out or in '''
        Sx = Sy = Sz = -1

        #choose which scaling transformation to do
        if mode == "out":
            Sx = Sy =Sz = 0.9
        elif mode == "in":
            Sx = Sy =Sz = 1.1

        mulMatrix = np.array(
            [[Sx, 0, 0, 0],
            [0, Sy, 0, 0],
            [0, 0, Sz, 0],
            [0, 0, 0, 1]]
        )
        coords = []

        for coord in self.coords:
            new_point = [float(coord[0]),float(coord[1]),float(coord[2]),1]
            tmp = np.matmul(new_point, mulMatrix)
            tmp = [float(x) for x in tmp]
            tmp =tmp[:-1]
            coords.append(tmp)
        self.coords = coords

    def rotation(self,direction,angle):
        ''' Rotation transformation multiplier every value
        with the mulMatrix that was build also by the wanted angle
        the direction by the wanted transformation: x,y,z '''
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
            new_point = [float(coord[0]),float(coord[1]),float(coord[2]),1]
            tmp = np.matmul(new_point, mulMatrix)
            tmp = [float(x) for x in tmp]
            tmp =tmp[:-1]
            coords.append(tmp)
        self.coords = coords




        

