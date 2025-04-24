from abc import ABC, abstractmethod
import numpy as np
from PyQt5.QtGui import QBrush, QPen
from PyQt5 import QtGui, QtCore

class GraphicObjectt(ABC):
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
        for coordenates in self.getPoints():
            x_center += coordenates[0]
            y_center += coordenates[1]

        return ([x_center/len(self.points), y_center/len(self.points)])


class Point(GraphicObjectt):
    def __init__(self, points):
        super().__init__(points)
        self.points = points
        self.center = self.calculateCenter()
        self.color = None

    def draw(self, viewport):
        self.id = viewport.scene().addEllipse(self.points[0][0], self.points[0][1], 5,5, QPen(self.color), QBrush(self.color))
        

    def translation(self, directions):
        new_points = []
        for coordenate in self.points:
            translation_matrix = [
                                [1,0,0],
                                [0,1,0],
                                [float(directions[0]), -float(directions[1]), 1]
                                        ]
            points_matrix = [coordenate[0], coordenate[1], 1]
            new_points.append(np.matmul(points_matrix, translation_matrix))

        self.points = new_points

        
    def escalonation(self, scale):
        new_points = []
        for coordenate in self.points:
            first_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [-(self.center[0]), -(self.center[1]), 1]
                                            ]

            second_translation_matrix = [[1, 0, 0],
                                    [0, 1, 0],
                                    [(self.center[0]), (self.center[1]), 1]
                                            ]
            
            escalonation_matrix = [
                                [scale[0], 0, 0],
                                [0, scale[1], 0],
                                [0,0,1]
                                        ]
            points_matrix = [coordenate[0], coordenate[1], 1]
            result = np.matmul(points_matrix, first_translation_matrix)
            result = np.matmul(result, escalonation_matrix)
            result = np.matmul(result, second_translation_matrix)
            new_points.append(result)

        self.points = new_points

    def rotationWord(self, angle, viewport):
        angle = (np.radians(angle))

        new_points = []
        for coordenate in self.points:
            rotation_matrix = [
                            [np.cos(angle), -(np.sin(angle)), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]
                                    ]
            points_matrix = [coordenate[0], coordenate[1], 1]
            result = np.matmul(points_matrix, rotation_matrix)
            new_points.append(result)

        self.points = new_points


    def rotationPoint(self, angle, point, viewport):
        angle = (np.radians(angle))

        new_points = []
        for coordenate in self.points:
            first_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [-(point[0]), -(point[1]), 1]
                                            ]
            
            rotaion_matrix = [
                            [np.cos(angle), -(np.sin(angle)), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]
                                    ]
            
            second_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [point[0], point[1], 1]
                                            ]
            
            points_matrix = [coordenate[0], coordenate[1], 1]
            
            result = np.matmul(points_matrix, first_translation_matrix)
            result = np.matmul(result, rotaion_matrix)
            result = np.matmul(result, second_translation_matrix)
            new_points.append(result)

        self.points = new_points


    def rotationCenter(self, angle, viewport):
        angle = (np.radians(angle))

        new_points = []
        for coordenate in self.points:
            first_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [-(self.center[0]), -(self.center[1]), 1]
                                            ]
            
            rotaion_matrix = [
                            [np.cos(angle), -(np.sin(angle)), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]
                                    ]
            
            second_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [self.center[0], self.center[1], 1]
                                            ]
            
            points_matrix = [coordenate[0], coordenate[1], 1]
            
            result = np.matmul(points_matrix, first_translation_matrix)
            result = np.matmul(result, rotaion_matrix)
            result = np.matmul(result, second_translation_matrix)
            new_points.append(result)

        self.points = new_points

class Line(GraphicObjectt):
    def __init__(self, points):
        super().__init__(points)
        self.points = points
        self.center = self.calculateCenter()
        self.color = None
        self.draw_points = points
        
    def draw(self, viewport):
        self.id = viewport.scene().addLine(self.draw_points[0][0], self.draw_points[0][1], self.draw_points[1][0], self.draw_points[1][1], QPen(self.color))
    
    def translation(self, directions):
        new_points = []
        for coordenate in self.points:
            translation_matrix = [
                                [1,0,0],
                                [0,1,0],
                                [float(directions[0]), -float(directions[1]), 1]
                                        ]
            points_matrix = [coordenate[0], coordenate[1], 1]
            new_points.append(np.matmul(points_matrix, translation_matrix))

        for i in range (len(self.points)):
            self.id.moveBy((new_points[i][0] - self.points[i][0]), (new_points[i][1] - self.points[i][1]))
        self.points = new_points   

    def escalonation(self, scale):
        new_points = []
        for coordenate in self.points:
            first_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [-(self.center[0]), -(self.center[1]), 1]
                                            ]

            second_translation_matrix = [[1, 0, 0],
                                    [0, 1, 0],
                                    [(self.center[0]), (self.center[1]), 1]
                                            ]
            
            escalonation_matrix = [
                                [scale[0], 0, 0],
                                [0, scale[1], 0],
                                [0,0,1]
                                        ]
            points_matrix = [coordenate[0], coordenate[1], 1]
            result = np.matmul(points_matrix, first_translation_matrix)
            result = np.matmul(result, escalonation_matrix)
            result = np.matmul(result, second_translation_matrix)
            new_points.append(result)

        self.points = new_points

    def rotationWord(self, angle):
        angle = (np.radians(angle))

        new_points = []
        for coordenate in self.points:
            rotation_matrix = [
                            [np.cos(angle), -(np.sin(angle)), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]
            ]
            points_matrix = [coordenate[0], coordenate[1], 1]
            result = np.matmul(points_matrix, rotation_matrix)
            new_points.append(result)

        self.points = new_points


    def rotationPoint(self, angle, point):
        angle = (np.radians(angle))

        new_points = []
        for coordenate in self.points:
            first_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [-(point[0]), -(point[1]), 1]
                                            ]
            
            rotaion_matrix = [
                            [np.cos(angle), -(np.sin(angle)), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]
                                    ]
            
            second_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [point[0], point[1], 1]
                                            ]
            
            points_matrix = [coordenate[0], coordenate[1], 1]
            
            result = np.matmul(points_matrix, first_translation_matrix)
            result = np.matmul(result, rotaion_matrix)
            result = np.matmul(result, second_translation_matrix)
            new_points.append(result)

        self.points = new_points


    def rotationCenter(self, angle):
        angle = (np.radians(angle))

        new_points = []
        for coordenate in self.points:
            first_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [-(self.center[0]), -(self.center[1]), 1]
                                            ]
            
            rotaion_matrix = [
                            [np.cos(angle), -(np.sin(angle)), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]
                                    ]
            
            second_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [self.center[0], self.center[1], 1]
                                            ]
            
            points_matrix = [coordenate[0], coordenate[1], 1]
            
            result = np.matmul(points_matrix, first_translation_matrix)
            result = np.matmul(result, rotaion_matrix)
            result = np.matmul(result, second_translation_matrix)
            new_points.append(result)

        self.points = new_points

class Polygon(GraphicObjectt):
    def __init__(self, points, filled = False):
        super().__init__(points)
        self.points = points
        self.center = self.calculateCenter()
        self.color = None
        self.filled = filled
        self.clipped_points = points.copy()
        
    def draw(self, viewport):
        points = self.clipped_points if hasattr(self, 'clipped_points') else self.points
        size = len(points)
        self.id = []
        if self.filled:
            polygon = QtGui.QPolygonF()
            for point in points:
                polygon.append(QtCore.QPointF(point[0], point[1]))
            self.id.append(viewport.scene().addPolygon(polygon, QPen(self.color), QBrush(self.color)))
        else:
            for i in range(size):
                self.id.append(viewport.scene().addLine(
                    points[i%size][0], points[i%size][1], 
                    points[(i+1)%size][0], points[(i+1)%size][1], 
                    QPen(self.color)))

    def applyClipping(self, clipping):
        self.clipped_points = clipping.polygonClipping(self)
        return self.on_screen

    def translation(self, directions):
        new_points = []
        for coordenate in self.points:
            translation_matrix = [
                                [1,0,0],
                                [0,1,0],
                                [float(directions[0]), -float(directions[1]), 1]
                                        ]
            points_matrix = [coordenate[0], coordenate[1], 1]
            new_points.append(np.matmul(points_matrix, translation_matrix))

        self.points = new_points

    def escalonation(self, scale):
        new_points = []
        for coordenate in self.points:
            first_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [-(self.center[0]), -(self.center[1]), 1]
                                            ]

            second_translation_matrix = [[1, 0, 0],
                                    [0, 1, 0],
                                    [(self.center[0]), (self.center[1]), 1]
                                            ]
            
            escalonation_matrix = [
                                [scale[0], 0, 0],
                                [0, scale[1], 0],
                                [0,0,1]
                                        ]
            points_matrix = [coordenate[0], coordenate[1], 1]
            result = np.matmul(points_matrix, first_translation_matrix)
            result = np.matmul(result, escalonation_matrix)
            result = np.matmul(result, second_translation_matrix)
            new_points.append(result)

        self.points = new_points

    def rotationWord(self, angle):
        angle = (np.radians(float(angle)))

        new_points = []
        for coordenate in self.points:
            rotation_matrix = [
                            [np.cos(angle), -(np.sin(angle)), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]
            ]
            points_matrix = [coordenate[0], coordenate[1], 1]
            result = np.matmul(points_matrix, rotation_matrix)
            new_points.append(result)

        self.points = new_points

    def rotationPoint(self, angle, point):
        angle = (np.radians(angle))

        new_points = []
        for coordenate in self.points:
            first_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [-(point[0]), -(point[1]), 1]
                                            ]
            
            rotaion_matrix = [
                            [np.cos(angle), -(np.sin(angle)), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]
                                    ]
            
            second_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [point[0], point[1], 1]
                                            ]
            
            points_matrix = [coordenate[0], coordenate[1], 1]
            
            result = np.matmul(points_matrix, first_translation_matrix)
            result = np.matmul(result, rotaion_matrix)
            result = np.matmul(result, second_translation_matrix)
            new_points.append(result)

        self.points = new_points


    def rotationCenter(self, angle):
        angle = (np.radians(angle))

        new_points = []
        for coordenate in self.points:
            first_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [-(self.center[0]), -(self.center[1]), 1]
                                            ]
            
            rotaion_matrix = [
                            [np.cos(angle), -(np.sin(angle)), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]
                                    ]
            
            second_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [self.center[0], self.center[1], 1]
                                            ]
            
            points_matrix = [coordenate[0], coordenate[1], 1]
            
            result = np.matmul(points_matrix, first_translation_matrix)
            result = np.matmul(result, rotaion_matrix)
            result = np.matmul(result, second_translation_matrix)
            new_points.append(result)

        self.points = new_points

class Curve(GraphicObjectt):
    def __init__(self, points, type):
        super().__init__(points)
        self.points = points
        self.center = self.calculateCenter()
        self.color = None
        self.cells = 100
        self.clipped_points_points = self.points.copy()
        self.type = type
        

    def draw(self,viewport):
        if (self.type == "BSpline"):
            points = self.clipped_points if hasattr(self, 'clipped_points') else self.bSpline()
        elif (self.type == "Bezier"):
            points = self.clipped_points if hasattr(self, 'clipped_points') else self.bezierAlgorithm()

        size = len(points)
        self.id = []

        for i in range(size-1):
            self.id.append(viewport.scene().addLine(
                    points[i][0], points[i][1], 
                    points[i+1][0], points[i+1][1], 
                    QPen(self.color)))


    def bezierAlgorithm(self):
        points = []        
        
        for bezier_points in self.getBezierPoints(self.points):
            while len(bezier_points) != 4:
                bezier_points.append([bezier_points[-1][0], bezier_points[-1][1]])

            for t in range(self.cells+1):
                t = t/self.cells
                P0_x = ((1-t) ** 3) * bezier_points[0][0]
                P0_y = ((1-t) ** 3) * bezier_points[0][1]

                P1_x = 3* ((1-t)**2) * t * bezier_points[1][0]
                P1_y = 3* ((1-t)**2) * t * bezier_points[1][1]

                P2_x = 3* (1-t) * (t**2) * bezier_points[2][0]
                P2_y = 3* (1-t) * (t**2) * bezier_points[2][1]

                P3_x = (t**3) * bezier_points[3][0]
                P3_y = (t**3) * bezier_points[3][1]

                x = P0_x + P1_x + P2_x + P3_x
                y = P0_y + P1_y + P2_y + P3_y

                points.append((x,y))

        return points
    
    def getBezierPoints(self, points):
        for i in range(0, len(points) - 1, 3):
            yield points[i : (i + 4)]


    def bSpline(self):
        points = []   
        b_spline_matrix = [
                            [-1/6, 1/2, -1/2, 1/6],
                            [1/2, -1, 1/2, 0],
                            [-1/2, 0, 1/2, 0],
                            [1/6, 2/3, 1/6, 0]
                            ]
        delta = 0.1
        delta3 = delta**3
        delta2 = delta**2
        n = 1 / delta
        E = [
            [0,0,0,1],
            [delta3, delta2, delta, 0],
            [6*delta3, 2*delta2, 0, 0],
            [6*delta3, 0, 0, 0]
            ]
        
        for b_points in self.getPointsBSplinePoints(self.points):
            mx = []
            my = []

            for coordinate in b_points:
                mx.append(coordinate[0])
                my.append(coordinate[1])

            coefficientsX = self.calculateCoefficientsMatrix(mx, b_spline_matrix)
            coefficientsY = self.calculateCoefficientsMatrix(my, b_spline_matrix)

            x,dx,dx2,dx3 = np.matmul(E, coefficientsX)
            y,dy,dy2,dy3 = np.matmul(E, coefficientsY)

            new_points = self.FwDifference(n, x, dx, dx2, dx3,
                                           y, dy, dy2, dy3)

            for p in new_points:
                points.append(p)

        return points
    
    def FwDifference(self, n, x, dx, dx2, dx3, 
                            y, dy, dy2, dy3):
        
        i = 0
        new_points = []

        while i < n:
            i += 1

            x += dx
            dx += dx2
            dx2 += dx3

            y += dy
            dy += dy2
            dy2 += dy3

            new_points.append((x,y))

        return new_points
    
    def calculateCoefficientsMatrix(self, M, G):
        C = np.matmul(G, M)
        return C

    def getPointsBSplinePoints(self, points):
        for i in range(len(points) - 3):
            yield points[i : (i + 4)]

    
    def applyClipping(self, clipping):
        if (self.type == "BSpline"):
            self.clipped_points = clipping.curveClipping(self, self.bSpline())
        elif (self.type == "Bezier"):
            self.clipped_points = clipping.curveClipping(self, self.bezierAlgorithm())
        return self.on_screen
    
    def translation(self, directions):
        new_points = []
        for coordenate in self.points:
            translation_matrix = [
                                [1,0,0],
                                [0,1,0],
                                [float(directions[0]), -float(directions[1]), 1]
                                        ]
            points_matrix = [coordenate[0], coordenate[1], 1]
            new_points.append(np.matmul(points_matrix, translation_matrix))

        self.points = new_points

    def escalonation(self, scale):
        new_points = []
        for coordenate in self.points:
            first_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [-(self.center[0]), -(self.center[1]), 1]
                                            ]

            second_translation_matrix = [[1, 0, 0],
                                    [0, 1, 0],
                                    [(self.center[0]), (self.center[1]), 1]
                                            ]
            
            escalonation_matrix = [
                                [scale[0], 0, 0],
                                [0, scale[1], 0],
                                [0,0,1]
                                        ]
            points_matrix = [coordenate[0], coordenate[1], 1]
            result = np.matmul(points_matrix, first_translation_matrix)
            result = np.matmul(result, escalonation_matrix)
            result = np.matmul(result, second_translation_matrix)
            new_points.append(result)

        self.points = new_points

    def rotationWord(self, angle):
        angle = (np.radians(float(angle)))

        new_points = []
        for coordenate in self.points:
            rotation_matrix = [
                            [np.cos(angle), -(np.sin(angle)), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]
            ]
            points_matrix = [coordenate[0], coordenate[1], 1]
            result = np.matmul(points_matrix, rotation_matrix)
            new_points.append(result)

        self.points = new_points

    def rotationPoint(self, angle, point):
        angle = (np.radians(angle))

        new_points = []
        for coordenate in self.points:
            first_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [-(point[0]), -(point[1]), 1]
                                            ]
            
            rotaion_matrix = [
                            [np.cos(angle), -(np.sin(angle)), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]
                                    ]
            
            second_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [point[0], point[1], 1]
                                            ]
            
            points_matrix = [coordenate[0], coordenate[1], 1]
            
            result = np.matmul(points_matrix, first_translation_matrix)
            result = np.matmul(result, rotaion_matrix)
            result = np.matmul(result, second_translation_matrix)
            new_points.append(result)

        self.points = new_points


    def rotationCenter(self, angle):
        angle = (np.radians(angle))

        new_points = []
        for coordenate in self.points:
            first_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [-(self.center[0]), -(self.center[1]), 1]
                                            ]
            
            rotaion_matrix = [
                            [np.cos(angle), -(np.sin(angle)), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]
                                    ]
            
            second_translation_matrix = [
                                    [1, 0, 0],
                                    [0, 1, 0],
                                    [self.center[0], self.center[1], 1]
                                            ]
            
            points_matrix = [coordenate[0], coordenate[1], 1]
            
            result = np.matmul(points_matrix, first_translation_matrix)
            result = np.matmul(result, rotaion_matrix)
            result = np.matmul(result, second_translation_matrix)
            new_points.append(result)

        self.points = new_points
        