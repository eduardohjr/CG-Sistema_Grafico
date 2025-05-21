import numpy as np
from graphicObject import *
from point3D import Point3D
from PyQt5.QtGui import QPen

class BezierSurface3D(GraphicObject):
    def __init__(self, patches):
        super().__init__([])
        self.patches = patches
        self.color = None
        self.on_screen = True

    def getPoints(self):
        points = []
        for patch in self.patches:
            for row in patch:
                for pt in row:
                    points.append(pt.points[0])
        return points

    def draw(self, viewport):
        if not self.on_screen:
            return

        self.id = []
        if hasattr(self, 'clipped_edges') and self.clipped_edges:
            for x1, y1, x2, y2 in self.clipped_edges:
                self.id.append(viewport.scene().addLine(x1, y1, x2, y2, QPen(self.color)))
        else:
            for patch in self.patches:
                self.draw_patch(patch, viewport)

    def draw_patch(self, control_points, viewport):
        steps = 10
        points_grid = [[None for _ in range(steps)] for _ in range(steps)]

        def bernstein(t):
            return [
                (1 - t)**3,
                3 * t * (1 - t)**2,
                3 * t**2 * (1 - t),
                t**3
            ]

        for i, u in enumerate(np.linspace(0, 1, steps)):
            Bu = bernstein(u)
            for j, v in enumerate(np.linspace(0, 1, steps)):
                Bv = bernstein(v)
                x = y = z = 0
                for m in range(4):
                    for n in range(4):
                        px, py, pz = control_points[m][n].points[0]
                        b = Bu[m] * Bv[n]
                        x += b * px
                        y += b * py
                        z += b * pz
                proj = Point3D([(x, y, z)]).projection()
                points_grid[i][j] = proj

        for i in range(steps):
            for j in range(steps - 1):
                x1, y1 = points_grid[i][j]
                x2, y2 = points_grid[i][j + 1]
                self.id.append(viewport.scene().addLine(x1, y1, x2, y2, QPen(self.color)))

        for j in range(steps):
            for i in range(steps - 1):
                x1, y1 = points_grid[i][j]
                x2, y2 = points_grid[i + 1][j]
                self.id.append(viewport.scene().addLine(x1, y1, x2, y2, QPen(self.color)))

    def applyClipping(self, clipping):
        return clipping.bezierSurfaceClipping(self)

    def translation(self, directions):
        for patch in self.patches:
            for row in patch:
                for pt in row:
                    pt.translation(directions)

    def escalonation(self, scale):
        cx = cy = cz = count = 0
        for patch in self.patches:
            for row in patch:
                for pt in row:
                    x, y, z = pt.points[0]
                    cx += x
                    cy += y
                    cz += z
                    count += 1
        cx /= count
        cy /= count
        cz /= count

        for patch in self.patches:
            for row in patch:
                for pt in row:
                    x, y, z = pt.points[0]
                    x = cx + (x - cx) * scale[0]
                    y = cy + (y - cy) * scale[1]
                    z = cz + (z - cz) * scale[2]
                    pt.points[0] = (x, y, z)

    def rotationWorld(self, angle, axis):
        for patch in self.patches:
            for row in patch:
                for pt in row:
                    pt.rotationWorld(angle, axis)

    def rotationPoint(self, angle, point, axis):
        for patch in self.patches:
            for row in patch:
                for pt in row:
                    pt.rotationPoint(angle, point, axis)

    def rotationCenter(self, angle, axis):
        cx = cy = cz = count = 0
        for patch in self.patches:
            for row in patch:
                for pt in row:
                    x, y, z = pt.points[0]
                    cx += x
                    cy += y
                    cz += z
                    count += 1
        center = (cx / count, cy / count, cz / count)
        self.rotationPoint(angle, center, axis)

    @staticmethod
    def from_text_input(text):
        patches = []
        raw_patches = text.strip().split("\n")
        for raw_patch in raw_patches:
            rows = raw_patch.strip().split(";")
            if len(rows) != 4:
                continue
            patch = []
            for row in rows:
                points = []
                for triplet in row.strip().split(")"):
                    triplet = triplet.strip().strip(",(")
                    if triplet:
                        x, y, z = map(float, triplet.split(","))
                        points.append(Point3D([(x, y, z)]))
                if len(points) == 4:
                    patch.append(points)
            if len(patch) == 4:
                patches.append(patch)
        return patches