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
        y_center = 0
        x_center = 0
        z_center = 0
        for coordenates in self.getPoints():
            x_center += coordenates[0]
            y_center += coordenates[1]
            try:
                z_center += coordenates[2]
            except:
                z_center = y_center

        return ([x_center/len(self.points), y_center/len(self.points), z_center/len(self.points)])
        