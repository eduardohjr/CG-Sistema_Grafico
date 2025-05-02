from graphicObject import *
from PyQt5.QtCore import Qt, QPointF, QLineF
from constants import CAM_DISTANCE

class Point3D(GraphicObject):
    def __init__(self, points):
        super().__init__(points)
        self.points = points
        self.center = self.calculateCenter()
        self.color = None


    def draw(self, viewport):
        projection = self.projection()
        self.id = viewport.scene().addEllipse(projection.x() , projection.y() - 3, 5, 5) 

    def projection(self):
        x = self.points[0][0]
        y = self.points[0][1]
        z = self.points[0][2]
        if z != 0:
            x_proj = (x * CAM_DISTANCE) / z
            y_proj = (y * CAM_DISTANCE) / z
        else:
            x_proj, y_proj = x, y
        return QPointF(x_proj, y_proj)
    

        
    def translation(self, directions):
        pass

    
    def escalonation(self, directions):
        pass
