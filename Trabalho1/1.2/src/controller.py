
from graphicObject import Point, Line, Polygon
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QVBoxLayout, QTabBar, QLabel, QLineEdit, QComboBox, QStackedWidget, QPushButton
from PyQt5.QtCore import Qt

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
            graphicObject.translation(input,self.__viewport)
            self.updateObject(graphicObject, index)

    def escalonateEvent(self, window):
        if(self.__tree.selectedIndexes()):
            index = self.__tree.selectedIndexes()[0].row()
            graphicObject =self.__viewport.objects[index]
            input = self.takeInputs(window)
            graphicObject.escalonation(input, self.__viewport)
            self.updateObject(graphicObject, index)

    def rotateEvent(self):
        if(self.__tree.selectedIndexes()):
            index = self.__tree.selectedIndexes()[0].row()
            graphicObject = self.__viewport.objects[index]
            self.selectRotation(graphicObject, index)


    def addTree(self, object):
        itemID = QStandardItem("graphicObject" + str(self.__current_id))
        itemCoordenates = QStandardItem(str(object.getPoints()))
        self.__model.setItem(self.treeIndex,0, itemID)
        self.__model.setItem(self.treeIndex,1, itemCoordenates)
        self.treeIndex += 1
        self.__current_id += 1

    def updateObject(self, object, index):
        newCoordenates = object.getPoints()
        object.center = object.calculateCenter()

        result = []
        for coordenate in newCoordenates:
            result.append((float(coordenate[0]), float(coordenate[1])))
        result = QStandardItem(str(result))
        self.__model.setItem(index,1, result)

    def selectRotation(self, graphicObject, index):
        self.dialog = QWidget()
        self.dialog.setWindowTitle("Choice of rotation")
        self.dialog.setGeometry(100, 100, 360, 150)

        layout = QVBoxLayout()
        self.tab_bar = QTabBar()
        self.tab_bar.setShape(QTabBar.RoundedNorth)
        self.tab_content = QStackedWidget()
        self.tab_bar.addTab("")
        self.tab_bar.addTab("Center of the world")
        self.tab_bar.addTab("center of the object")
        self.tab_bar.addTab("Any point")

        self.setupTab1()
        self.rotateOnWorld(graphicObject, index)
        self.rotateOnCenter(graphicObject, index)
        self.rotateOnPoint(graphicObject, index)

        self.tab_bar.currentChanged.connect(self.tab_content.setCurrentIndex)
        layout.addWidget(self.tab_bar, alignment=Qt.AlignLeft)
        layout.addWidget(self.tab_content)
        self.dialog.setLayout(layout)
        self.dialog.show()

    def setupTab1(self):
        tab1_content = QLabel("Select a rotation above")
        tab1_content.setAlignment(Qt.AlignCenter)
        self.tab_content.addWidget(tab1_content)

    def rotateOnWorld(self, graphicObject, index):
        tab2_widget = QWidget()
        tab2_layout = QVBoxLayout()
        helper_text = QLabel("Enter the point and angle for the object to be rotated:")
        helper_text.setAlignment(Qt.AlignCenter)
        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("Enter the angle here...")
        execute_button = QPushButton("Execute")
        execute_button.clicked.connect(lambda : self.executeRotWorld(graphicObject, index))
        tab2_layout.addWidget(helper_text)
        tab2_layout.addWidget(self.angle_input)
        tab2_layout.addWidget(execute_button)
        tab2_layout.setAlignment(Qt.AlignCenter)
        tab2_widget.setLayout(tab2_layout)
        self.tab_content.addWidget(tab2_widget)

    def rotateOnCenter(self, graphicObject, index):
        tab2_widget = QWidget()
        tab2_layout = QVBoxLayout()
        helper_text = QLabel("Enter the point and angle for the object to be rotated:")
        helper_text.setAlignment(Qt.AlignCenter)
        self.angle_input2 = QLineEdit()
        self.angle_input2.setPlaceholderText("Enter the angle here...")
        execute_button = QPushButton("Execute")
        execute_button.clicked.connect(lambda: self.executeRotCenter(graphicObject, index))
        tab2_layout.addWidget(helper_text)
        tab2_layout.addWidget(self.angle_input2)
        tab2_layout.addWidget(execute_button)
        tab2_layout.setAlignment(Qt.AlignCenter)
        tab2_widget.setLayout(tab2_layout)
        self.tab_content.addWidget(tab2_widget)

    def rotateOnPoint(self, graphicObject, index):
        tab2_widget = QWidget()
        tab2_layout = QVBoxLayout()
        helper_text = QLabel("Enter the point and angle for the object to be rotated:")
        helper_text.setAlignment(Qt.AlignCenter)
        self.angle_input3 = QLineEdit()
        self.angle_input3.setPlaceholderText("Ex: x,y,45")
        execute_button = QPushButton("Execute")
        execute_button.clicked.connect(lambda: self.executeRotPoint(graphicObject, index))
        tab2_layout.addWidget(helper_text)
        tab2_layout.addWidget(self.angle_input3)
        tab2_layout.addWidget(execute_button)
        tab2_layout.setAlignment(Qt.AlignCenter)
        tab2_widget.setLayout(tab2_layout)
        self.tab_content.addWidget(tab2_widget)

    def executeRotWorld(self, object, index):
        angle = self.angle_input.text()
        try:

            object.rotationWord(float(angle), self.__viewport)
            self.updateObject(object, index)
            self.dialog.destroy()
        except:
            self.instructionsPopUp

    def executeRotCenter(self, object, index):
        angle = self.angle_input2.text()
        try:
            object.rotationCenter(float(angle), self.__viewport)
            self.updateObject(object, index)
            self.dialog.destroy()
        except:
            self.instructionsPopUp()

    def executeRotPoint(self, object, index):
        inputs = self.angle_input3.text()
        try:
            inputs = tuple(map(float, inputs.split(',')))
            angle = inputs[2]
            points = [inputs[i] for i in range(0,2)]
            if (len(inputs) == 3):
                object.rotationPoint(angle, points, self.__viewport)
                self.updateObject(object, index)
                self.dialog.destroy()
            else:
                self.commaPopUp(2)
        except:
            self.instructionsPopUp()
        

    def takeInputs(self, window):
        coordenates, done = QInputDialog.getText(
            window, 'Input Dialog', 'Give points like this -> x,y :') 

        if done :
            try:
                coordenates = tuple(map(float, coordenates.split(',')))
                if (len(coordenates) == 2):
                    return coordenates
                else:
                    self.commaPopUp(1)
            except:
                self.instructionsPopUp()
            
    def instructionsPopUp(self):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR")
        msg.setText("ERROR! Please follow the instructions")
        msg.setIcon(QMessageBox.Warning)

        x = msg.exec_()

    def commaPopUp(self, type):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR")
        if type == 1:
            msg.setText("Give only one coordenate (x,y) \n"
                        "Use '.' to separate fractional numbers")
        elif type == 2:
            msg.setText("Give only one coordenate (x,y) and one angle (n)\n"
                        "Use '.' to separate fractional numbers")
            
        msg.setIcon(QMessageBox.Question)
        x = msg.exec_()





