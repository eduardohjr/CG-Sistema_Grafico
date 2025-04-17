from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QLineEdit, QCheckBox
from constants import *
from viewport import View
from controller import Controller
from treeView import Tree
from normalizedWindow import NormalizedWindow
from PyQt5 import QtGui, QtCore
from radioButton import RadioButton


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(APP_NAME)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)        
        
        self.viewport = View(self)
        self.viewport.setGeometry(VIEWPORT_XPOS, VIEWPORT_YPOS, VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
        self.viewport.setStyleSheet("background-color: lightgrey")

        self.tree = Tree(self)
        self.tree.setGeometry(TREE_XPOS, TREE_YPOS, TREE_WIDTH, TREE_HEIGHT)

        self.controller = Controller(self.viewport, self.tree)
        self.createButtons()

        self.normalizedWindow = NormalizedWindow(self.viewport)
        self.normalizedWindow.delimiteViewport()

        self.line_edit = QLineEdit(self.normalizedWindow.clipping.lineClippingType, parent=self)
        self.line_edit.setReadOnly(True)
        self.line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.line_edit.setGeometry(330,40, (BUTTON_WIDTH*2), 20)

        self.radioButton = RadioButton()


        self.show()

    def closeEvent(self, event):
        self.radioButton.close()

    def createButtons(self):
        up = QPushButton(self)
        up.setText("UP")
        up.setGeometry(100,310,BUTTON_WIDTH,BUTTON_HEIGHT)
        up.clicked.connect(lambda: self.controller.upEvent(self.normalizedWindow))

        down = QPushButton(self)
        down.setText("DOWN")
        down.setGeometry(100,370,BUTTON_WIDTH,BUTTON_HEIGHT)
        down.clicked.connect(lambda: self.controller.downEvent(self.normalizedWindow))

        left = QPushButton(self)
        left.setText("LEFT")
        left.setGeometry(70,340,BUTTON_WIDTH,BUTTON_HEIGHT)
        left.clicked.connect(lambda: self.controller.leftEvent(self.normalizedWindow))

        right = QPushButton(self)
        right.setText("RIGHT")
        right.setGeometry(130,340,BUTTON_WIDTH,BUTTON_HEIGHT)
        right.clicked.connect(lambda: self.controller.rightEvent(self.normalizedWindow))

        zoom_in = QPushButton(self)
        zoom_in.setText("IN")
        zoom_in.setGeometry(230,310,BUTTON_WIDTH,BUTTON_HEIGHT)
        zoom_in.clicked.connect(lambda: self.controller.zoomInEvent(self.normalizedWindow))

        zoom_out = QPushButton(self)
        zoom_out.setText("OUT")
        zoom_out.setGeometry(230,360,BUTTON_WIDTH,BUTTON_HEIGHT)
        zoom_out.clicked.connect(lambda: self.controller.zoomOutEvent(self.normalizedWindow))
        
        self.filled_checkbox = QCheckBox("Filled Polygon", self)
        self.filled_checkbox.setGeometry(30, 45, 120, 20)

        curve_check_box = QCheckBox("Draw Curve", self)
        curve_check_box.setGeometry(150, 45, 120, 20)

        draw = QPushButton(self)
        draw.setText("Draw")
        draw.setGeometry(30,10,(BUTTON_WIDTH*2), BUTTON_HEIGHT)
        draw.clicked.connect(lambda: self.controller.drawEvent(
            self.normalizedWindow, 
            self.filled_checkbox.isChecked(),
            curve_check_box.isChecked()
        ))

        clear = QPushButton(self)
        clear.setText("Clear")
        clear.setGeometry(180, 10, (BUTTON_WIDTH*2), BUTTON_HEIGHT)
        clear.clicked.connect(self.controller.clearEvent)

        translate = QPushButton(self)
        translate.setText("Translate")
        translate.setGeometry(60, 440, (BUTTON_WIDTH*2), BUTTON_HEIGHT)
        translate.clicked.connect(lambda : self.controller.translateEvent(self))

        escalonate = QPushButton(self)
        escalonate.setText("Escalonate")
        escalonate.setGeometry(190, 440, (BUTTON_WIDTH*2), BUTTON_HEIGHT)
        escalonate.clicked.connect(lambda : self.controller.escalonateEvent(self))

        rotate_object = QPushButton(self)
        rotate_object.setText("Rotate Object")
        rotate_object.setGeometry(320, 440, (BUTTON_WIDTH*2), BUTTON_HEIGHT)
        rotate_object.clicked.connect(lambda : self.controller.rotateObjectEvent(self.normalizedWindow))

        rotate_window_left = QPushButton(self)
        rotate_window_left.setGeometry(330,340,(BUTTON_WIDTH), BUTTON_HEIGHT)
        rotate_window_left.setIcon(QtGui.QIcon("../icon/rotateIconLeft.png"))
        rotate_window_left.clicked.connect(lambda: self.controller.rotateWindowLeft(self.normalizedWindow))
        
        rotate_window_right = QPushButton(self)
        rotate_window_right.setGeometry(390, 340, (BUTTON_WIDTH), BUTTON_HEIGHT)
        rotate_window_right.setIcon(QtGui.QIcon("../icon/rotateIconRight.png"))
        rotate_window_right.clicked.connect(lambda: self.controller.rotateWindowRight(self.normalizedWindow))

        save_obj = QPushButton(self)
        save_obj.setText("Save .OBJ")
        save_obj.setGeometry(60, 480, (BUTTON_WIDTH*2), BUTTON_HEIGHT)
        save_obj.clicked.connect(self.saveToObj)

        load_obj = QPushButton(self)
        load_obj.setText("Load.OBJ")
        load_obj.setGeometry(190, 480, (BUTTON_WIDTH*2), BUTTON_HEIGHT)
        load_obj.clicked.connect(self.loadFromObj)

        select_clipping = QPushButton(self)
        select_clipping.setText("Select Clipping")
        select_clipping.setGeometry(330, 10, (BUTTON_WIDTH*2), BUTTON_HEIGHT)
        select_clipping.clicked.connect(self.showClippingRadioButton)






    def mousePressEvent(self, event):
        self.tree.clearSelection()
        self.tree.clearFocus()
        self.line_edit.clearFocus()
    
    def saveToObj(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Arquivo OBJ",
            "",
            "Arquivos OBJ (*.obj);;Todos os arquivos (*)"
        )
        if filename:
            if not filename.endswith('.obj'):
                filename += '.obj'
            
            if self.tree.selectedIndexes():
                index = self.tree.selectedIndexes()[0].row()
                self.controller.saveToObj(filename, index)
            else:
                self.controller.saveToObj(filename)

    def loadFromObj(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir Arquivo OBJ",
            "",
            "Arquivos OBJ (*.obj);;Todos os arquivos (*)"
        )
        if filename:
            self.controller.loadFromObj(filename)

    def showClippingRadioButton(self):
        self.radioButton.createClippingOptions(self.normalizedWindow.clipping, self.line_edit)
        self.radioButton.show()


        
        
        
        