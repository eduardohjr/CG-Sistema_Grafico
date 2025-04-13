from PyQt5.QtWidgets import *

class RadioButton(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.selected = None
        self.radioLayout = QGridLayout()
        self.setLayout(self.radioLayout)
        self.setFixedSize(230,50)
        self.setWindowTitle("Clipping Slect")

    def createClippingOptions(self, clipping, line_edit):
        radiobutton = QRadioButton("CS")
        radiobutton.selected = "CS"
        radiobutton.toggled.connect(lambda: self.onClicked(clipping, line_edit))
        self.radioLayout.addWidget(radiobutton, 0, 0)

        radiobutton = QRadioButton("LB")
        radiobutton.selected = "LB"
        radiobutton.toggled.connect(lambda: self.onClicked(clipping, line_edit))
        self.radioLayout.addWidget(radiobutton, 0, 1)

    def onClicked(self, clipping, line_edit):
        radioButton = self.sender()
        if radioButton.isChecked():
            clipping.lineClippingType = radioButton.selected
            line_edit.setText(radioButton.selected)
