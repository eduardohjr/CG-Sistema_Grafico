from graphicObject import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem
import constants as const

class Point3D(GraphicObject):
    def __init__(self, points):
        super().__init__(points)
        self.points = points
        self.color = None
        self.on_screen = True

    def draw(self, viewport):
        if not self.on_screen:
            return
         
        self.center = self.calculateCenter()
        x, y = self.projection()     
        radius = 4
        
        self.id = QGraphicsEllipseItem(x - radius, y - radius, radius * 2, radius * 2)
        self.id.setBrush(QBrush(self.color))
        viewport.scene().addItem(self.id)

    def projection(self):

        x, y, z = self.points[0]
        d = const.CAM_DISTANCE

        point = np.array([x, y, z, 1])
        m_per = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1/d, 0]
        ])

        result = m_per @ point
        w = result[3]
        if w == 0:
            w = 1e-5

        x_ndc = result[0] / w
        y_ndc = result[1] / w
        
        return x_ndc, y_ndc

    def translation(self, directions):

        dx, dy, dz = directions

        T = np.array([
            [1, 0, 0, dx],
            [0, 1, 0, -dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ])

        x, y, z = self.points[0]
        points_matrix = np.array([x, y, z, 1])

        result = T @ points_matrix

        self.points[0] = result[:3]

    def escalonation(self, scale):
        self.center = self.calculateCenter()
        cx = self.center[0]
        cy = self.center[1]
        cz = self.center[2]

        T1 = np.array([
            [1, 0, 0, -cx],
            [0, 1, 0, -cy],
            [0, 0, 1, -cz],
            [0, 0, 0, 1]
        ])

        S = np.array([
            [scale[0], 0,  0,  0],
            [0,  scale[1], 0,  0],
            [0,  0,  scale[2], 0],
            [0,  0,  0,  1]
        ])

        T2 = np.array([
            [1, 0, 0, cx],
            [0, 1, 0, cy],
            [0, 0, 1, cz],
            [0, 0, 0, 1]
        ])

        transform = T2 @ S @ T1

        x, y, z = self.points[0]
        points_matrix = np.array([x, y, z, 1])
        result = transform @ points_matrix

        self.points[0] = result[:3]


    def rotationWorld(self, angle, axis):

        angle = np.radians(angle)
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)

        if axis == 'x':
            R = np.array([
                [1,     0,      0,     0],
                [0,  cos_a, -sin_a,  0],
                [0,  sin_a,  cos_a,  0],
                [0,     0,      0,     1]
            ])
        elif axis == 'y':
            R = np.array([
                [cos_a,  0, sin_a, 0],
                [0,      1,    0,  0],
                [-sin_a, 0, cos_a, 0],
                [0,      0,    0,  1]
            ])
        elif axis == 'z':
            R = np.array([
                [cos_a, -sin_a, 0, 0],
                [sin_a,  cos_a, 0, 0],
                [0,         0,  1, 0],
                [0,         0,  0, 1]
            ])
        else:
            raise ValueError("Invalid axis. Use 'x', 'y', or 'z'.")

        x, y, z = self.points[0]
        points_matrix = np.array([x, y, z, 1])
        resukt = R @ points_matrix
        self.points[0] = resukt[:3]


    def rotationPoint(self, angle, point, axis):

        px, py, pz = point
        angle = np.radians(angle)
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)

        T1 = np.array([
            [1, 0, 0, -px],
            [0, 1, 0, -py],
            [0, 0, 1, -pz],
            [0, 0, 0, 1]
        ])

        T2 = np.array([
            [1, 0, 0, px],
            [0, 1, 0, py],
            [0, 0, 1, pz],
            [0, 0, 0, 1]
        ])

        if axis == 'x':
            R = np.array([
                [1,     0,      0,     0],
                [0,  cos_a, -sin_a,  0],
                [0,  sin_a,  cos_a,  0],
                [0,     0,      0,     1]
            ])
        elif axis == 'y':
            R = np.array([
                [cos_a,  0, sin_a, 0],
                [0,      1,    0,  0],
                [-sin_a, 0, cos_a, 0],
                [0,      0,    0,  1]
            ])
        elif axis == 'z':
            R = np.array([
                [cos_a, -sin_a, 0, 0],
                [sin_a,  cos_a, 0, 0],
                [0,         0,  1, 0],
                [0,         0,  0, 1]
            ])
        else:
            raise ValueError("Invalid axis. Use 'x', 'y', or 'z'.")

        transform = T2 @ R @ T1
        x, y, z = self.points[0]
        points_matrix = np.array([x, y, z, 1])
        result = transform @ points_matrix
        self.points[0] = result[:3]


    def rotationCenter(self, angle, axis):
        self.rotationPoint(angle, self.center, axis)

    def applyClipping(self, clipping):
        clipping.pointClippingCheck(self)