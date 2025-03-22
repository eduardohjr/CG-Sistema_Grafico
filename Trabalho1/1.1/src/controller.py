
from graphicObject import Point, Line, Polygon
from PyQt5.QtGui import QStandardItem

class Controller():
    def __init__(self, viewport, tree):
        self.__viewport = viewport
        self.__scene = self.__viewport.scene()
        self.__tree = tree
        self.__model = self.__tree.model
        self.__current_id = 1
        self.move_multiplier = 20
        self.zoomIn_mutiplier = 1.1
        self.zoomOut_multiplier = 0.9
        self.treeIndex = 0

    def drawEvent(self):
        self.clearText()

        object = None

        if (len(self.__viewport.coordenates) == 0):
            print("Nenhum ponto selecionado")

        elif (len(self.__viewport.coordenates) == 1):
            object = Point(self.__viewport.coordenates, self.__current_id)
        elif (len(self.__viewport.coordenates) == 2):
            object = Line(self.__viewport.coordenates, self.__current_id)
        else:
            object = Polygon(self.__viewport.coordenates, self.__current_id)

        self.__current_id += 1
        self.__viewport.objects.append(object)
        object.draw(self.__viewport)

        self.updateTree(object)
        self.__viewport.coordenates.clear()


    def clearText(self):
        for element in self.__viewport.text:
            self.__scene.removeItem(element)
        self.__viewport.text.clear()


    def clearEvent(self):
        if (not self.__viewport.objects):
            self.clearText()
            self.__viewport.coordenates.clear()
        else:
            self.__scene .clear() #AQUI DA ERRO SE DER CLEAR DEPOIS DE SO SELECIONAR OS PONTS
            self.__viewport.coordenates.clear()
            self.__viewport.objects.clear()
            self.__current_id = 1
            self.treeIndex = 0
            self.__model.removeRows(0, self.__model.rowCount())

    def checkMovent(self):
        if (not self.__viewport.coordenates):
            return True
        else:
            return False

    def upEvent(self):
        if(self.checkMovent()):
            for item in self.__scene .items():
                item.moveBy(0, self.move_multiplier)

    def downEvent(self):
        if(self.checkMovent()):
            for item in self.__scene .items():
                item.moveBy(0, (-self.move_multiplier))

    def rightEvent(self):
        if(self.checkMovent()):
            for item in self.__scene .items():
                item.moveBy((-self.move_multiplier), 0)

    def leftEvent(self):
        if(self.checkMovent()):
            for item in self.__scene .items():
                item.moveBy(self.move_multiplier, 0)

    def updateTree(self, object):
        itemID = QStandardItem(str(object.getId()))
        itemCoordenates = QStandardItem(str(object.getPoints()))
        self.__model.setItem(self.treeIndex,0, itemID)
        self.__model.setItem(self.treeIndex,1, itemCoordenates)
        self.treeIndex += 1

    def zoomInEvent(self):
        self.__viewport.scale(self.zoomIn_mutiplier, self.zoomIn_mutiplier)
    
    def zoomOutEvent(self):
        self.__viewport.scale(self.zoomOut_multiplier, self.zoomOut_multiplier)


