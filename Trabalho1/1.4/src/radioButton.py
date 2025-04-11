from PyQt5.QtWidgets import *

class RadioButton(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.selected = None
        self.radioLayout = QGridLayout()
        self.setLayout(self.radioLayout)
        self.setFixedSize(230,50)
        self.setWindowTitle("Clipping Slect")

    def createClippingOptions(self, clipping):
        radiobutton = QRadioButton("CS")
        radiobutton.setChecked(True)
        radiobutton.selected = "CS"
        radiobutton.toggled.connect(lambda: self.onClicked(clipping))
        self.radioLayout.addWidget(radiobutton, 0, 0)

        radiobutton = QRadioButton("LB")
        radiobutton.selected = "LB"
        radiobutton.toggled.connect(lambda: self.onClicked(clipping))
        self.radioLayout.addWidget(radiobutton, 0, 1)

    def onClicked(self, clipping):
        radioButton = self.sender()
        if radioButton.isChecked():
            clipping.lineClippingType = radioButton.selected
