import numpy as np
from graphicObject import *
from point3D import Point3D
from PyQt5.QtGui import QPen
from constants import STEPS

class BSplineSurface3D(GraphicObject):
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
            for x0, y0, x1, y1 in self.clipped_edges:
                self.id.append(viewport.scene().addLine(x0, y0, x1, y1, QPen(self.color)))
            return

        for patch in self.patches:
            self.draw_patch(patch, viewport)

    def draw_patch(self, patch, viewport):
        def bspline_basis_matrix():
            return (1/6) * np.array([
                [-1, 3, -3, 1],
                [3, -6, 3, 0],
                [-3, 0, 3, 0],
                [1, 4, 1, 0]
            ])

        def delta_matrix(d):
            d2 = d * d
            d3 = d2 * d
            return np.array([
                [0, 0, 0, 1],
                [d3, d2, d, 0],
                [6*d3, 2*d2, 0, 0],
                [6*d3, 0, 0, 0]
            ])

        def fwd_diff(n, x, dx, d2x, d3x, y, dy, d2y, d3y, z, dz, d2z, d3z):
            pts = [[x, y, z]]
            for _ in range(1, n):
                x += dx
                dx += d2x
                d2x += d3x

                y += dy
                dy += d2y
                d2y += d3y

                z += dz
                dz += d2z
                d2z += d3z

                pts.append([x, y, z])
            return pts

        delta = 1 / (STEPS - 1)
        E = delta_matrix(delta)
        Et = E.T
        M = bspline_basis_matrix()

        Gx = np.array([[pt.points[0][0] for pt in row] for row in patch])
        Gy = np.array([[pt.points[0][1] for pt in row] for row in patch])
        Gz = np.array([[pt.points[0][2] for pt in row] for row in patch])

        Cx = M @ Gx @ M.T
        Cy = M @ Gy @ M.T
        Cz = M @ Gz @ M.T

        DDx = E @ Cx @ Et
        DDy = E @ Cy @ Et
        DDz = E @ Cz @ Et

        mesh_rows = []
        for i in range(STEPS):
            x, dx, d2x, d3x = DDx[0]
            y, dy, d2y, d3y = DDy[0]
            z, dz, d2z, d3z = DDz[0]
            pts = fwd_diff(STEPS, x, dx, d2x, d3x, y, dy, d2y, d3y, z, dz, d2z, d3z)
            row = [Point3D([p]).projection() for p in pts]
            mesh_rows.append(row)

            for k in range(3):
                DDx[k] += DDx[k+1]
                DDy[k] += DDy[k+1]
                DDz[k] += DDz[k+1]

        for i in range(STEPS):
            for j in range(STEPS - 1):
                x1, y1 = mesh_rows[i][j]
                x2, y2 = mesh_rows[i][j + 1]
                self.id.append(viewport.scene().addLine(x1, y1, x2, y2, QPen(self.color)))

            DDx = E @ Cx @ Et
        DDy = E @ Cy @ Et
        DDz = E @ Cz @ Et

        DDx = DDx.T
        DDy = DDy.T
        DDz = DDz.T

        mesh_cols = []
        for j in range(STEPS):
            x, dx, d2x, d3x = DDx[0]
            y, dy, d2y, d3y = DDy[0]
            z, dz, d2z, d3z = DDz[0]
            pts = fwd_diff(STEPS, x, dx, d2x, d3x, y, dy, d2y, d3y, z, dz, d2z, d3z)
            col = [Point3D([p]).projection() for p in pts]
            mesh_cols.append(col)

            for k in range(3):
                DDx[k] += DDx[k+1]
                DDy[k] += DDy[k+1]
                DDz[k] += DDz[k+1]

        for j in range(STEPS):
            for i in range(STEPS - 1):
                x1, y1 = mesh_cols[j][i]
                x2, y2 = mesh_cols[j][i + 1]
                self.id.append(viewport.scene().addLine(x1, y1, x2, y2, QPen(self.color)))


    def applyClipping(self, clipping):
        return clipping.bSplineSurfaceClipping(self)

    @staticmethod
    def from_text_input(text):
        lines = text.strip().split(";")
        matrix = []
        for line in lines:
            row = []
            for p in line.strip().split("),"):
                p = p.replace("(", "").replace(")", "").strip()
                if p:
                    x, y, z = map(float, p.split(","))
                    row.append(Point3D([(x, y, z)]))
            matrix.append(row)
        matrix = np.array(matrix, dtype=object)
        m, n = matrix.shape
        patches = []
        for i in range(0, m - 3, 3):
            for j in range(0, n - 3, 3):
                patch = matrix[i:i+4, j:j+4]
                patches.append(patch)
        return patches
    

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