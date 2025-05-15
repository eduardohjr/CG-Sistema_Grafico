from graphicObject import *
from point3D import Point3D
from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtCore import Qt


class Object3D(GraphicObject):
    def __init__(self, points, segments):
        super().__init__(points)
        self.points = points
        self.color = None
        self.segments = segments

    def getPoints(self):
        return [p.points[0] for p in self.points]

    def draw(self, viewport):
        self.id = []

        if hasattr(self, 'clipped_edges') and self.clipped_edges:
            for x1, y1, x2, y2 in self.clipped_edges:
                line = QGraphicsLineItem(x1, y1, x2, y2)
                line.setPen(QPen(self.color))
                self.id.append(line)
                viewport.scene().addItem(line)
        else:
            for i1, i2 in self.segments:
                p1 = self.points[i1]
                p2 = self.points[i2]
                x1, y1 = p1.projection()
                x2, y2 = p2.projection()

                line = QGraphicsLineItem(x1, y1, x2, y2)
                line.setPen(QPen(self.color))
                self.id.append(line)
                viewport.scene().addItem(line)

    def translation(self, directions):
        dx = float(directions[0])
        dy = float(directions[1])
        dz = float(directions[2])

        translation_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [dx, -dy, dz, 1] 
        ])


        for point_obj in self.points:
            x, y, z = point_obj.points[0]
            point_matrix = np.array([x, y, z, 1])
            result = point_matrix @ translation_matrix
            point_obj.points[0] = (result[0], result[1], result[2])

    
    def escalonation(self, scale_factors):
        sx = float(scale_factors[0])
        sy = float(scale_factors[1])
        sz = float(scale_factors[2])

        scaling_matrix = np.array([
            [sx, 0,  0,  0],
            [0,  sy, 0,  0],
            [0,  0,  sz, 0],
            [0,  0,  0,  1]
        ])

        for point_obj in self.points:
            x, y, z = point_obj.points[0]
            point_matrix = np.array([x, y, z, 1])
            result = point_matrix @ scaling_matrix
            point_obj.points[0] = (result[0], result[1], result[2])

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

        for point in self.points:
            x, y, z = point.points[0]
            points_matrix = np.array([x, y, z, 1])
            result = points_matrix @ R
            point.points[0] = (result[0], result[1], result[2])

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

        for point in self.points:
            x, y, z = point.points[0]
            points_matrix = np.array([x, y, z, 1])
            result = transform @ points_matrix
            point.points[0] = (result[0], result[1], result[2])


    def rotationCenter(self, angle, axis):
        xs, ys, zs = zip(*[point.points[0] for point in self.points])
        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)
        cz = sum(zs) / len(zs)

        self.rotationPoint(angle, (cx, cy, cz), axis)

    def applyClipping(self, clipping):
        self.clipped_edges = []

        for edge in self.segments:
            p1 = self.points[edge[0]]
            p2 = self.points[edge[1]]

            x1, y1 = p1.projection()
            x2, y2 = p2.projection()

            clipped = clipping.clippingSegments((x1, y1), (x2, y2))
            if clipped:
                self.clipped_edges.append(clipped)

        self.on_screen = len(self.clipped_edges) > 0