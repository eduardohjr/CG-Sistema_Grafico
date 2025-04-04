from PyQt5 import QtCore
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from constants import *

class View(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent)
        self.setScene(QGraphicsScene(self))
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        self.pen = QPen(QtCore.Qt.black)
        self.redPen = QPen(QtCore.Qt.red)
        self.blackBurh = QBrush(QtCore.Qt.black)
        self.redBurh = QBrush(QtCore.Qt.red)
        self.coordenates = []
        self.objects = []
        self.text = []
        
        
    def mousePressEvent(self, event):
        self.position = event.pos()
        point = QtCore.QPointF(self.mapToScene(self.position))
        self.coordenates.append((point.x(), point.y()))
        text = self.scene().addSimpleText(
            "*"+str((point.x(), point.y()))
        )
        text.setBrush(QtCore.Qt.red)
        text.setPos(point)
        self.text.append(text)


    