import numpy as np
from point import Point
from line import Line
from polygon import Polygon
from curve import Curve
from point3D import Point3D
from object3D import Object3D
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

    def calculate_transformation(self, point, infos):
        translation = infos[0]
        scale = infos[1]
        rotation = infos[2]

        rx, ry, rz = np.radians(rotation)

        T = np.array([
            [1, 0, 0, translation[0]],
            [0, 1, 0, translation[1]],
            [0, 0, 1, translation[2]],
            [0, 0, 0, 1]
        ])

        S = np.array([
            [scale[0], 0, 0, 0],
            [0, scale[1], 0, 0],
            [0, 0, scale[2], 0],
            [0, 0, 0, 1]
        ])

        Rx = np.array([
            [1, 0, 0, 0],
            [0, np.cos(rx), -np.sin(rx), 0],
            [0, np.sin(rx),  np.cos(rx), 0],
            [0, 0, 0, 1]
        ])

        Ry = np.array([
            [np.cos(ry), 0, np.sin(ry), 0],
            [0, 1, 0, 0],
            [-np.sin(ry), 0, np.cos(ry), 0],
            [0, 0, 0, 1]
        ])

        Rz = np.array([
            [np.cos(rz), -np.sin(rz), 0, 0],
            [np.sin(rz),  np.cos(rz), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        transform = T @ Rz @ Ry @ Rx @ S

        if len(point) == 2:
            point = np.array([point[0], point[1], 0, 1])
        else:
            point = np.array([point[0], point[1], point[2], 1])

        result = transform @ point
        return result[:3] 
    
    def normalize(self, obj, infos):

        new_points = []
        previous_on_screen = obj.on_screen

        for p in obj.getPoints():
            if len(p) == 2:
                p = [p[0], p[1], 0]
            result = self.calculate_transformation(p, infos)
            
            new_points.append(Point3D([(result[0], result[1], result[2])]))

        if isinstance(obj, Object3D):
            obj.points = new_points

            obj.applyClipping(self.clipping)
            if obj.on_screen:
                obj.center = obj.calculateCenter()
                if previous_on_screen:
                    for item in obj.id:
                        self.viewport.scene().removeItem(item)
                obj.draw(self.viewport)
            else:
                if previous_on_screen:
                    for item in obj.id:
                        self.viewport.scene().removeItem(item)
        else:
            flat_points = []
            for p in new_points:
                flat_points.append([p.points[0][0], p.points[0][1]])

            obj.points = flat_points.copy()

            if isinstance(obj, Point):
                self.clipping.pointClippingCheck(obj)
            elif isinstance(obj, Line):
                obj.draw_points = self.clipping.lineClipping(obj)
            else:
                obj.applyClipping(self.clipping)

            if obj.on_screen:
                obj.center = obj.calculateCenter()
                if isinstance(obj, (Polygon, Curve)):
                    if previous_on_screen:
                        for item in obj.id:
                            self.viewport.scene().removeItem(item)
                    obj.draw(self.viewport)
                else:
                    if previous_on_screen:
                        self.viewport.scene().removeItem(obj.id)
                    obj.draw(self.viewport)
            else:
                if previous_on_screen:
                    if isinstance(obj, (Polygon, Curve)):
                        for item in obj.id:
                            self.viewport.scene().removeItem(item)
                    else:
                        self.viewport.scene().removeItem(obj.id)



    def delimiteViewport(self):
        self.viewport.scene().addRect(VIEWPORT_DELIMITION_XPOS,VIEWPORT_DELIMITION_YPOS, VIEWPORT_DELIMITION_WIDTH, VIEWPORT_DELIMITION_HEIGHT, self.viewport.redPen)

    

