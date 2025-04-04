import numpy as np
from graphicObject import Polygon

class NormalizedWindow:
    def __init__(self, viewport):
        self.viewport = viewport

    def calculate_transformation(self, points, infos):
        windowCoord = infos[0]
        scale = infos[1]
        angle = infos[2]
        rad_angle = (np.radians(angle))


        translation_matrix = [
                            [1,0,0],
                            [0,1,0],
                            [-(windowCoord[0]), (-windowCoord[1]), 1]
                                    ]
        
        rotation_matrix = [
                        [np.cos(rad_angle), -(np.sin(rad_angle)), 0],
                        [np.sin(rad_angle), np.cos(rad_angle), 0],
                        [0, 0, 1]
                                    ]
        
        escalonation_matrix = [
                    [scale[0], 0, 0],
                    [0, scale[1], 0],
                    [0,0,1]
                            ]
        
        result = np.matmul(points, translation_matrix)
        result = np.matmul(result, rotation_matrix)
        result = np.matmul(result, escalonation_matrix)

        return result
    
    def normalize(self, object, infos):
        new_points = []
        
        for coordinates in object.getPoints():
            points_matrix = [coordinates[0], coordinates[1], 1]
            result = self.calculate_transformation(points_matrix, infos)
            new_points.append(result)

            object.points = new_points.copy()

        if (isinstance(object, Polygon)):
            for item in object.id:
                self.viewport.scene().removeItem(item)
            object.draw(self.viewport)
            
        else:
            self.viewport.scene().removeItem(object.id)
            object.draw(self.viewport)


    def delimiteViewport(self):
        self.viewport.scene().addRect(-400,-240, 900, 500, self.viewport.redPen)