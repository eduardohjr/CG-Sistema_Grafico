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
