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

    def lineClipping(self, Gobject):
        if self.lineClippingType == "CS":
            return self.CsClipping(Gobject)
        else:
            pass


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
                                object.clipped = True
                                new_points[index][1] = points[index][1]
                                break
                        else:
                            new_points[index][0] = x
                    
                    if y != None:
                        if not (self.minY< y < self.maxY):
                            if x == None:
                                object.clipped = True
                                new_points[index][0] = points[index][0]
                                break
                        else:
                            new_points[index][1] = y

        return new_points