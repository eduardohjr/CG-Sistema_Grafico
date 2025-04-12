import numpy as np
from graphicObject import Polygon, Point, Line
from clipping import Clipping
from constants import *

class NormalizedWindow:
    def __init__(self, viewport):
        self.viewport = viewport
        self.minX = VIEWPORT_DELIMITION_XPOS
        self.minY = VIEWPORT_DELIMITION_YPOS
        self.maxX = (VIEWPORT_DELIMITION_WIDTH - abs(self.minX))
        self.maxY = (VIEWPORT_DELIMITION_HEIGHT - abs(self.minY))
        self.clipping = Clipping(self.minX, self.minY, self.maxX, self.maxY)

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

        previous_on_screen = object.on_screen
        
        for coordinates in object.getPoints():
            points_matrix = [coordinates[0], coordinates[1], 1]
            result = self.calculate_transformation(points_matrix, infos)
            new_points.append(result)

            object.points = new_points.copy()

        if (isinstance(object, Point)):
            self.clipping.pointClippingCheck(object)
        elif (isinstance(object, Line)):
            object.draw_points = self.clipping.lineClipping(object)


        if (object.on_screen):
            object.center = object.calculateCenter()

            if (isinstance(object, Polygon)):
                for item in object.id:
                    self.viewport.scene().removeItem(item)
                object.draw(self.viewport)
                
            else:
                if(previous_on_screen):
                    self.viewport.scene().removeItem(object.id)
                object.draw(self.viewport)

        else:
            if (previous_on_screen):
                self.viewport.scene().removeItem(object.id)


    def delimiteViewport(self):
        self.viewport.scene().addRect(VIEWPORT_DELIMITION_XPOS,VIEWPORT_DELIMITION_YPOS, VIEWPORT_DELIMITION_WIDTH, VIEWPORT_DELIMITION_HEIGHT, self.viewport.redPen)

    

