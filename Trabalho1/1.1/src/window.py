from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
import constants as const
import view
from controller import Controller


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(const.APP_NAME)
        self.setFixedSize(const.WINDOW_WIDTH, const.WINDOW_HEIGHT)        
        
        self.viewport = view.View(self)
        self.viewport.setGeometry(const.VIEWPORT_XPOS, const.VIEWPORT_YPOS, const.VIEWPORT_WIDTH, const.VIEWPORT_HEIGHT)
        self.viewport.setStyleSheet("background-color: lightgrey")

        self.controller = Controller(self.viewport)

        self.createButtons()

        self.show()

    def createButtons(self):
        up = QtWidgets.QPushButton(self)
        up.setText("UP")
        up.setGeometry(100,310,const.BUTTON_WIDTH,const.BUTTON_HEIGHT)

        down = QtWidgets.QPushButton(self)
        down.setText("DOWN")
        down.setGeometry(100,370,const.BUTTON_WIDTH,const.BUTTON_HEIGHT)

        left = QtWidgets.QPushButton(self)
        left.setText("LEFT")
        left.setGeometry(70,340,const.BUTTON_WIDTH,const.BUTTON_HEIGHT)

        right = QtWidgets.QPushButton(self)
        right.setText("RIGHT")
        right.setGeometry(130,340,const.BUTTON_WIDTH,const.BUTTON_HEIGHT)

        zoom_in = QtWidgets.QPushButton(self)
        zoom_in.setText("IN")
        zoom_in.setGeometry(230,310,const.BUTTON_WIDTH,const.BUTTON_HEIGHT)
        zoom_in.clicked.connect(self.controller.zoomInEffect)

        zoom_out = QtWidgets.QPushButton(self)
        zoom_out.setText("OUT")
        zoom_out.setGeometry(230,360,const.BUTTON_WIDTH,const.BUTTON_HEIGHT)

        draw = QtWidgets.QPushButton(self)
        draw.setText("Draw")
        draw.setGeometry(30,10,(const.BUTTON_WIDTH*2), const.BUTTON_HEIGHT)
        draw.clicked.connect(self.controller.drawEvent)

        clear = QtWidgets.QPushButton(self)
        clear.setText("Clear")
        clear.setGeometry(180, 10, (const.BUTTON_WIDTH*2), const.BUTTON_HEIGHT)
        clear.clicked.connect(self.controller.clearEvent)


