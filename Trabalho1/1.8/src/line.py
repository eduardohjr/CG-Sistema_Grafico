from graphicObject import *

class Line(GraphicObject):
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

    def rotationWorld(self, angle, axis=None):
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