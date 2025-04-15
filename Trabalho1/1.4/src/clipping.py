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
        # Sutherland-Hodgman algorithm for polygon clipping
        def clip(subject_polygon, clip_polygon):
            def inside(p, edge):
                # try:
                #     x, y = p
                # except:
                #     x,y,z = p
                x1, y1, x2, y2 = edge
                return (x2 - x1) * (p[1] - y1) > (y2 - y1) * (p[0] - x1)

            def compute_intersection(p1, p2, edge):
                # try:
                #     x1, y1 = p1
                #     x2, y2 = p2
                # except:
                #     x1, y1, z1 = p1
                #     x2, y2, z2 = p2

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

        clipped_points = clip(polygon.points, [])
        if not clipped_points:
            polygon.on_screen = False
            return []
        
        polygon.on_screen = True
        return clipped_points
