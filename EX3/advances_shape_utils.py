
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
        
        for poly in self.polygons:
            print(poly)
        

class Polygon:
    def __init__(self, coords):
        self.coords = coords
        
        self.zValue = coords[0][2]
        for cord in coords[1:]:
            if cord[2] > self.zValue:
                self.zValue = cord[2]
        self.color = 'black'

    def __str__(self):
        return "Coords = {}\nzValues = {}\nColor = {}\n".format(self.coords, self.zValue, self.color)

