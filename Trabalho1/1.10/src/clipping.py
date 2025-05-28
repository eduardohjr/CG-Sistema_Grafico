from polygon import Polygon
from point3D import Point3D
import numpy as np
from constants import STEPS

class Clipping():
    def __init__(self, minX, minY, maxX, maxY):
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY
        self.lineClippingType = "CS"

    def pointClippingCheck(self, object):
        points = object.points[0]
        x = points[0]
        y = points[1]

        if (x < self.minX) or (x > self.maxX) or (y < self.minY) or (y >self.maxY):
            object.on_screen = False
        else :
            object.on_screen = True

    def lineClipping(self, object):
        if self.lineClippingType == "CS":
            return self.CsClipping(object)
        else:
            return self.LbClipping(object)


    def CsClipping(self, object):
        points = object.points

        RC = [[None]*4 for _ in range(len(points))]
        intersect_different_sectors = False

        new_points= [[points[0][0], points[0][1]], [points[1][0], points[1][1]]]

        for index, coordinates in enumerate(points):
            if (coordinates[0] < self.minX) :
                RC[index][3] = 1
            else:
                RC[index][3] = 0

            if (coordinates[0] > self.maxX) :
                RC[index][2] = 1
            else:
                RC[index][2] = 0

            if (coordinates[1] < self.minY) :
                RC[index][1] = 1
            else:
                RC[index][1] = 0

            if (coordinates[1] > self.maxY) :
                RC[index][0] = 1
            else:
                RC[index][0] = 0


        if (RC[0] == [0,0,0,0] and RC[1] == [0,0,0,0]):
            object.on_screen = True
        elif [RC0 and RC1 for RC0, RC1 in zip(RC[0], RC[1])] != [0,0,0,0] :
            object.on_screen = False
        elif [RC0 and RC1 for RC0, RC1 in zip(RC[0], RC[1])] == [0,0,0,0] :
            object.on_screen = True
            intersect_different_sectors = True

        if (intersect_different_sectors):
            m = (points[1][1]-points[0][1]) / (points[1][0] - points[0][0])

            for index, position in enumerate(RC):
                    x = None
                    y = None
                    if position[0] == 1:
                        x = points[index][0] + (1 / m) * (self.maxY - points[index][1])
                        new_points[index][1] = self.maxY
                    if position[1] == 1:
                        x = points[index][0] + (1 / m )* (self.minY- points[index][1])
                        new_points[index][1] = self.minY
                    if position[2] == 1:
                        y = m * (self.maxX - points[0][0]) + points[0][1]
                        new_points[index][0] = self.maxX
                    if position[3] == 1:
                        y = m * (self.minX - points[0][0]) + points[0][1]
                        new_points[index][0] = self.minX

                    if x != None:
                        if not (self.minX < x < self.maxX):
                            if y == None:
                                object.on_screen = False
                                new_points[index][1] = points[index][1]
                                break
                        else:
                            new_points[index][0] = x
                    
                    if y != None:
                        if not (self.minY< y < self.maxY):
                            if x == None:
                                object.on_screen = False
                                new_points[index][0] = points[index][0]
                                break
                        else:
                            new_points[index][1] = y

        return new_points
    
    def LbClipping(self, object):
        points = object.points

        p = [None] * 4
        q = [None] * 4
        zeta = [None] * 2
        r = [[], []]
        
        new_points = [[points[0][0], points[0][1]], [points[1][0], points[1][1]]]
        object.on_screen = True
        
        p[0] = -(points[1][0] - points[0][0])
        p[1] = points[1][0] - points[0][0]
        p[2] = -(points[1][1] - points[0][1])
        p[3] = points[1][1] - points[0][1]

        q[0] = points[0][0] - self.minX
        q[1] = self.maxX - points[0][0]
        q[2] = points[0][1] - self.minY
        q[3] = self.maxY - points[0][1]

        for i, element in enumerate(p):
            if element == 0:
                if q[i] < 0:
                    object.on_screen = False
                else:
                    return new_points
            elif element < 0:
                r[0].append(q[i] / element)
            else:
                r[1].append(q[i] / element)

        if object.on_screen:
            zeta[0] = max(0, r[0][0], r[0][1])
            zeta[1] = min(1, r[1][0], r[1][1])

            if zeta[0] > zeta[1]:
                object.on_screen = False
            else:
                if zeta[0] != 0:
                    new_points[0][0] = points[0][0] + (zeta[0] * p[1])
                    new_points[0][1] = points[0][1] + (zeta[0] * p[3])

                if zeta[1] != 1:
                    new_points[1][0] = points[0][0] + (zeta[1] * p[1])
                    new_points[1][1] = points[0][1] + (zeta[1] * p[3])

        return new_points

    def polygonClipping(self, polygon):
        def clip(subject_polygon, clip_polygon):
            def inside(p, edge):
                x1, y1, x2, y2 = edge
                return (x2 - x1) * (p[1] - y1) > (y2 - y1) * (p[0] - x1)

            def compute_intersection(p1, p2, edge):
                x3, y3, x4, y4 = edge
                
                denom = (y4 - y3) * (p2[0] - p1[0]) - (x4 - x3) * (p2[1] - p1[1])
                if denom == 0:
                    return p1
                    
                ua = ((x4 - x3) * (p1[1] - y3) - (y4 - y3) * (p1[0] - x3)) / denom
                return (
                    p1[0] + ua * (p2[0] - p1[0]),
                    p1[1] + ua * (p2[1] - p1[1])
                )

            edges = [
                (self.minX, self.minY, self.maxX, self.minY),
                (self.maxX, self.minY, self.maxX, self.maxY),
                (self.maxX, self.maxY, self.minX, self.maxY),
                (self.minX, self.maxY, self.minX, self.minY)
            ]
            
            output_polygon = subject_polygon
            for edge in edges:
                input_polygon = output_polygon
                output_polygon = []
                if not input_polygon:
                    break
                    
                prev_point = input_polygon[-1]
                for curr_point in input_polygon:
                    if inside(curr_point, edge):
                        if not inside(prev_point, edge):
                            intersection = compute_intersection(prev_point, curr_point, edge)
                            output_polygon.append(intersection)
                        output_polygon.append(curr_point)
                    elif inside(prev_point, edge):
                        intersection = compute_intersection(prev_point, curr_point, edge)
                        output_polygon.append(intersection)
                    prev_point = curr_point
            
            return output_polygon

        if isinstance(polygon, Polygon):
            clipped_points = clip(polygon.points, [])
        else:
            clipped_points = clip(polygon.bezierAlgorithm(), [])
        if not clipped_points:
            polygon.on_screen = False
            return []
        
        polygon.on_screen = True
        return clipped_points
    
    def curveClipping(self, curve, points):
        def clip(subject_polygon, clip_polygon):
            def inside(p, edge):
                x1, y1, x2, y2 = edge
                return (x2 - x1) * (p[1] - y1) > (y2 - y1) * (p[0] - x1)

            edges = [
                (self.minX, self.minY, self.maxX, self.minY),
                (self.maxX, self.minY, self.maxX, self.maxY),
                (self.maxX, self.maxY, self.minX, self.maxY),
                (self.minX, self.maxY, self.minX, self.minY)
            ]
            
            output_polygon = subject_polygon
            for edge in edges:
                input_polygon = output_polygon
                output_polygon = []
                if not input_polygon:
                    break
                    
                for curr_point in input_polygon:
                    if inside(curr_point, edge):
                        output_polygon.append(curr_point)

            return output_polygon

        
        clipped_points = clip(points, [])
        if not clipped_points:
            curve.on_screen = False
            return []
        
        curve.on_screen = True
        return clipped_points
    
    def object3DClippingCheck(self, object3D):
        object3D.on_screen = False 

        for point in object3D.getPoints():
            if hasattr(point, 'projection'):
                x_proj, y_proj = point.projection()

                if (self.minX <= x_proj <= self.maxX) and (self.minY <= y_proj <= self.maxY):
                    object3D.on_screen = True
                    return

    def clippingSegments(self, p0, p1):
        x0, y0 = p0
        x1, y1 = p1

        dx = x1 - x0
        dy = y1 - y0

        p = [-dx, dx, -dy, dy]
        q = [x0 - self.minX, self.maxX - x0, y0 - self.minY, self.maxY - y0]

        u1 = 0.0
        u2 = 1.0

        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    return None
            else:
                r = q[i] / p[i]
                if p[i] < 0:
                    u1 = max(u1, r)
                else:
                    u2 = min(u2, r)

        if u1 > u2:
            return None

        x0_clip = x0 + u1 * dx
        y0_clip = y0 + u1 * dy
        x1_clip = x0 + u2 * dx
        y1_clip = y0 + u2 * dy

        return (x0_clip, y0_clip, x1_clip, y1_clip)
    
    def clipping3dpoint(self, obj):
        if hasattr(obj, 'projection'):
            x, y = obj.projection()
        else:
            x, y = obj.points[0]

        if (x < self.minX) or (x > self.maxX) or (y < self.minY) or (y > self.maxY):
            obj.on_screen = False
        else:
            obj.on_screen = True


    def bezierSurfaceClipping(self, surface):
        surface.on_screen = False
        surface.clipped_edges = []

        for patch in surface.patches:
            grid = [[None for _ in range(STEPS)] for _ in range(STEPS)]

            def bernstein(t):
                return [
                    (1 - t) ** 3,
                    3 * t * (1 - t) ** 2,
                    3 * t ** 2 * (1 - t),
                    t ** 3
                ]

            for i, u in enumerate(np.linspace(0, 1, STEPS)):
                Bu = bernstein(u)
                for j, v in enumerate(np.linspace(0, 1, STEPS)):
                    Bv = bernstein(v)
                    x = y = z = 0
                    for m in range(4):
                        for n in range(4):
                            px, py, pz = patch[m][n].points[0]
                            b = Bu[m] * Bv[n]
                            x += b * px
                            y += b * py
                            z += b * pz
                    grid[i][j] = Point3D([(x, y, z)])

            for i in range(STEPS):
                for j in range(STEPS - 1):
                    p1 = grid[i][j].projection()
                    p2 = grid[i][j+1].projection()
                    clipped = self.clippingSegments(p1, p2)
                    if clipped:
                        surface.clipped_edges.append(clipped)
                        surface.on_screen = True

            for j in range(STEPS):
                for i in range(STEPS - 1):
                    p1 = grid[i][j].projection()
                    p2 = grid[i+1][j].projection()
                    clipped = self.clippingSegments(p1, p2)
                    if clipped:
                        surface.clipped_edges.append(clipped)
                        surface.on_screen = True
    

    def bSplineSurfaceClipping(self, surface):
        surface.clipped_edges = []
        surface.on_screen = False

        for patch in surface.patches:
            def bspline_basis_matrix():
                return (1 / 6) * np.array([
                    [-1, 3, -3, 1],
                    [3, -6, 3, 0],
                    [-3, 0, 3, 0],
                    [1, 4, 1, 0]
                ])

            def delta_matrix(delta):
                d2 = delta * delta
                d3 = delta * d2
                return np.array([
                    [0, 0, 0, 1],
                    [d3, d2, delta, 0],
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
                row = [Point3D([p]) for p in pts]
                mesh_rows.append(row)

                for k in range(3):
                    DDx[k] += DDx[k+1]
                    DDy[k] += DDy[k+1]
                    DDz[k] += DDz[k+1]

            for i in range(STEPS):
                for j in range(STEPS - 1):
                    p1 = mesh_rows[i][j].projection()
                    p2 = mesh_rows[i][j+1].projection()
                    clipped = self.clippingSegments(p1, p2)
                    if clipped:
                        surface.clipped_edges.append(clipped)
                        surface.on_screen = True

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
                col = [Point3D([p]) for p in pts]
                mesh_cols.append(col)

                for k in range(3):
                    DDx[k] += DDx[k+1]
                    DDy[k] += DDy[k+1]
                    DDz[k] += DDz[k+1]

            for i in range(STEPS):
                for j in range(STEPS - 1):
                    p1 = mesh_cols[i][j].projection()
                    p2 = mesh_cols[i][j+1].projection()
                    clipped = self.clippingSegments(p1, p2)
                    if clipped:
                        surface.clipped_edges.append(clipped)
                        surface.on_screen = True
