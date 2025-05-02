from graphicObject import *
from point3D import Point3D
from PyQt5.QtCore import Qt, QPointF, QLineF

class Object3D(GraphicObject):
    def __init__(self, points, segments):
        super().__init__(points)
        self.points = points
        self.center = self.calculateCenter()
        self.color = None
        self.segments = segments

    def draw(self, viewport):
        self.transformSegments()
        project = self.projection()
        self.id = []
        for p1_proj, p2_proj in project:
            line = QLineF(p1_proj, p2_proj)
            self.id.append(viewport.scene().addLine(line))

    def transformSegments(self):
        transformed_segments = []
        for segment in self.segments:
            c1 = segment[0]
            c2 = segment[1]
            transformed_segments.append([Point3D([c1]), Point3D([c2])])

        self.segments = transformed_segments

    def projection(self):
        project = []
        for p1, p2 in self.segments:
            p1_proj = p1.projection()
            p2_proj = p2.projection()
            project.append((p1_proj, p2_proj))
        return project


    def translation(self, directions):
        pass

    
    def escalonation(self, directions):
        pass