from abc import ABC, abstractmethod

class GraphicObjectt(ABC):
    @abstractmethod
    def __init__(self, points, id):
        self.__id = None
        self.__points = []

    def getId(self):
        return self.__id
    
    def getPoints(self):
        return self.__points
    
    @abstractmethod
    def draw(self, viewport):
        pass

class Point(GraphicObjectt):
    def __init__(self, points,id):
        self.__points = points
        self.__id = id

    def draw(self, viewport):
        viewport.scene().addEllipse(self.__points[0][0], self.__points[0][1], 5,5, viewport.pen, viewport.blackBurh)

class Line(GraphicObjectt):
    def __init__(self, points, id):
        self.__points = points
        self.__id =id

    def draw(self, viewport):
        viewport.scene().addLine(self.__points[0][0], self.__points[0][1], self.__points[1][0], self.__points[1][1])

class Polygon(GraphicObjectt):
    def __init__(self, points, id):
        self.__points = points
        self.__ids =id

    def draw(self, viewport):
        points = self.__points
        size = len(points)
        for i in range(size):
            viewport.scene().addLine(points[i%size][0], points[i%size][1], points[(i+1)%size][0], points[(i+1)%size][1])
        
