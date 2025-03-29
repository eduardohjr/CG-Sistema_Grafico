
from PyQt5.QtWidgets import QMainWindow, QPushButton
import constants as const
from viewport import View
from controller import Controller
from treeView import Tree


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(const.APP_NAME)
        self.setFixedSize(const.WINDOW_WIDTH, const.WINDOW_HEIGHT)        
        
        self.viewport = View(self)
        self.viewport.setGeometry(const.VIEWPORT_XPOS, const.VIEWPORT_YPOS, const.VIEWPORT_WIDTH, const.VIEWPORT_HEIGHT)
        self.viewport.setStyleSheet("background-color: lightgrey")

        self.tree = Tree(self)
        self.tree.setGeometry(const.TREE_XPOS, const.TREE_YPOS, const.TREE_WIDTH, const.TREE_HEIGHT)

        self.controller = Controller(self.viewport, self.tree)
        self.createButtons()

        self.show()

    def createButtons(self):
        up = QPushButton(self)
        up.setText("UP")
        up.setGeometry(100,310,const.BUTTON_WIDTH,const.BUTTON_HEIGHT)
        up.clicked.connect(self.controller.upEvent)

        down = QPushButton(self)
        down.setText("DOWN")
        down.setGeometry(100,370,const.BUTTON_WIDTH,const.BUTTON_HEIGHT)
        down.clicked.connect(self.controller.downEvent)

        left = QPushButton(self)
        left.setText("LEFT")
        left.setGeometry(70,340,const.BUTTON_WIDTH,const.BUTTON_HEIGHT)
        left.clicked.connect(self.controller.leftEvent)

        right = QPushButton(self)
        right.setText("RIGHT")
        right.setGeometry(130,340,const.BUTTON_WIDTH,const.BUTTON_HEIGHT)
        right.clicked.connect(self.controller.rightEvent)

        zoom_in = QPushButton(self)
        zoom_in.setText("IN")
        zoom_in.setGeometry(230,310,const.BUTTON_WIDTH,const.BUTTON_HEIGHT)
        zoom_in.clicked.connect(self.controller.zoomInEvent)

        zoom_out = QPushButton(self)
        zoom_out.setText("OUT")
        zoom_out.setGeometry(230,360,const.BUTTON_WIDTH,const.BUTTON_HEIGHT)
        zoom_out.clicked.connect(self.controller.zoomOutEvent)
        
        draw = QPushButton(self)
        draw.setText("Draw")
        draw.setGeometry(30,10,(const.BUTTON_WIDTH*2), const.BUTTON_HEIGHT)
        draw.clicked.connect(self.controller.drawEvent)

        clear = QPushButton(self)
        clear.setText("Clear")
        clear.setGeometry(180, 10, (const.BUTTON_WIDTH*2), const.BUTTON_HEIGHT)
        clear.clicked.connect(self.controller.clearEvent)

        translate = QPushButton(self)
        translate.setText("Translate")
        translate.setGeometry(60, 440, (const.BUTTON_WIDTH*2), const.BUTTON_HEIGHT)
        translate.clicked.connect(lambda : self.controller.translateEvent(self))

        escalonate = QPushButton(self)
        escalonate.setText("Escalonate")
        escalonate.setGeometry(190, 440, (const.BUTTON_WIDTH*2), const.BUTTON_HEIGHT)
        escalonate.clicked.connect(lambda : self.controller.escalonateEvent(self))

        rotate = QPushButton(self)
        rotate.setText("Rotate")
        rotate.setGeometry(320, 440, (const.BUTTON_WIDTH*2), const.BUTTON_HEIGHT)
        rotate.clicked.connect(self.controller.rotateEvent)


    def mousePressEvent(self, event):
        self.tree.clearSelection()
        self.tree.clearFocus()
        

        