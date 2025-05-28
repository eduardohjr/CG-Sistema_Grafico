from abc import ABC, abstractmethod
import numpy as np
from PyQt5.QtGui import QBrush, QPen
from PyQt5 import QtGui, QtCore

class GraphicObject(ABC):
    @abstractmethod
    def __init__(self, points):
        self.id = None
        self.points = []
        self.draw_points = []
        self.center = None
        self.color = None
        self.on_screen = True

    def getId(self):
        return self.id
    
    def getPoints(self):
        return self.points
    
    @abstractmethod
    def translation(self, directions):
        pass

    @abstractmethod
    def escalonation(self, directions):
        pass

    @abstractmethod
    def draw(self, viewport):
        pass

    def calculateCenter(self):
        x_center = y_center = z_center = 0
        points = self.getPoints()

        if len(points) == 0:
            return [0, 0, 0]

        for coord in points:
            x_center += coord[0]
            y_center += coord[1]
            try:
                z_center += coord[2]
            except :
                z_center += y_center

        count = len(points)
        return [x_center / count, y_center / count, z_center / count]
        