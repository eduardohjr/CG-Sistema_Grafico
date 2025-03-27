
from graphicObject import Point, Line, Polygon
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QInputDialog, QMessageBox


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
        if (self.__viewport.coordenates):
            self.clearText()

            object = None

            if (len(self.__viewport.coordenates) == 1):
                object = Point(self.__viewport.coordenates.copy())
            elif (len(self.__viewport.coordenates) == 2):
                object = Line(self.__viewport.coordenates.copy())
            else:
                object = Polygon(self.__viewport.coordenates.copy())

            self.__viewport.objects.append(object)
            object.draw(self.__viewport)

            self.addTree(object)
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
            self.__scene .clear()
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

    def zoomInEvent(self):
        self.__viewport.scale(self.zoomIn_mutiplier, self.zoomIn_mutiplier)
    
    def zoomOutEvent(self):
        self.__viewport.scale(self.zoomOut_multiplier, self.zoomOut_multiplier)

    def translateEvent(self, window):
        if(self.__tree.selectedIndexes()):
            index = self.__tree.selectedIndexes()[0].row()
            graphicObject = self.__viewport.objects[index]
            input = self.takeInputs(window)
            graphicObject.translation(input)
            self.updateTree(graphicObject, index)

    def escalonateEvent(self, window):
        if(self.__tree.selectedIndexes()):
            index = self.__tree.selectedIndexes()[0].row()
            graphicObject =self.__viewport.objects[index]
            input = self.takeInputs(window)
            graphicObject.escalonation(input, self.__viewport)
            self.updateTree(graphicObject, index)

    def addTree(self, object):
        itemID = QStandardItem("graphicObject" + str(self.__current_id))
        itemCoordenates = QStandardItem(str(object.getPoints()))
        self.__model.setItem(self.treeIndex,0, itemID)
        self.__model.setItem(self.treeIndex,1, itemCoordenates)
        self.treeIndex += 1
        self.__current_id += 1

    def updateTree(self, object, index):
        newCoordenates = object.getPoints()
        result = []
        for coordenate in newCoordenates:
            result.append((float(coordenate[0]), float(coordenate[1])))
        result = QStandardItem(str(result))
        self.__model.setItem(index,1, result)

    def takeInputs(self, window):
        coordenates, done1 = QInputDialog.getText(
            window, 'Input Dialog', 'Give scale like this -> x,y :') 

        if done1 :
            try:
                coordenates = tuple(map(float, coordenates.split(',')))
                if (len(coordenates) == 2):
                    return coordenates
                else:
                    self.commaPopUp()
            except:
                self.instructionsPopUp()
            
        
    def instructionsPopUp(self):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR")
        msg.setText("ERROR! Please follow the instructions")
        msg.setIcon(QMessageBox.Warning)

        x = msg.exec_()

    def commaPopUp(self):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR")
        msg.setText("Give only one coordenate (x,y) \n"
                    "Use '.' to separate fractional numbers")
        msg.setIcon(QMessageBox.Question)

        x = msg.exec_()





