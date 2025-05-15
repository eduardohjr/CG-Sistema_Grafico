from graphicObject import *


class Polygon(GraphicObject):
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

    def rotationWorld(self, angle, axis=None):
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

    def rotationPoint(self, angle, point, axis=None):
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


    def rotationCenter(self, angle, axis=None):
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