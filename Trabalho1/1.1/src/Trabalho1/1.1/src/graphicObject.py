from abc import ABC, abstractmethod

class GraphicObjectt(ABC):
    @abstractmethod
    def __init__(self, points, id):
        self.id = None
        self.points = []

    def getId(self):
        return self.id
    
    def getPoints(self):
        return self.points
    
    @abstractmethod
    def draw(self, viewport):
        pass

class Point(GraphicObjectt):
    def __init__(self, points,id):
        self.points = points
        self.id = id

    def draw(self, viewport):
        viewport.scene().addEllipse(self.points[0][0], self.points[0][1], 5,5, viewport.pen, viewport.blackBurh)

class Line(GraphicObjectt):
    def __init__(self, points, id):
        self.points = points
        self.id =id

    def draw(self, viewport):
        viewport.scene().addLine(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1])

class Polygon(GraphicObjectt):
    def __init__(self, points, id):
        self.points = points
        self.id=id

    def draw(self, viewport):
        points = self.points
        size = len(points)
        for i in range(size):
            viewport.scene().addLine(points[i%size][0], points[i%size][1], points[(i+1)%size][0], points[(i+1)%size][1])
        
