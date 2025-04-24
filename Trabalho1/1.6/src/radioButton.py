from PyQt5.QtWidgets import *

class RadioButton():
    def __init__(self):
        self.clipping_widget = QWidget()
        self.clipping_widget.selected = None
        self.layout1 = QGridLayout()
        self.clipping_widget.setLayout(self.layout1)
        self.clipping_widget.setFixedSize(230,50)
        self.clipping_widget.setWindowTitle("Clipping Slect")

        self.curve_widget = QWidget()
        self.curve_widget.selected = None
        self.layout2 = QGridLayout()
        self.curve_widget.setLayout(self.layout2)
        self.curve_widget.setFixedSize(230,50)
        self.curve_widget.setWindowTitle("Curve Slect")

    def createClippingOptions(self, clipping, line_edit):
        radiobutton = QRadioButton("CS")
        radiobutton.selected = "CS"
        radiobutton.toggled.connect(lambda: self.onClickedClipping(line_edit, clipping))
        self.layout1.addWidget(radiobutton, 0, 0)

        radiobutton = QRadioButton("LB")
        radiobutton.selected = "LB"
        radiobutton.toggled.connect(lambda: self.onClickedClipping(line_edit, clipping))
        self.layout1.addWidget(radiobutton, 0, 1)

    def createCurveOptions(self, controller, line_edit):
        radiobutton = QRadioButton("Bezier")
        radiobutton.selected = "Bezier"
        radiobutton.toggled.connect(lambda: self.onClickedCurve(line_edit, controller))
        self.layout2.addWidget(radiobutton, 0, 0)

        radiobutton = QRadioButton("BSpline")
        radiobutton.selected = "BSpline"
        radiobutton.toggled.connect(lambda: self.onClickedCurve(line_edit, controller))
        self.layout2.addWidget(radiobutton, 0, 1)


    def onClickedClipping(self, line_edit, clipping):
        radioButton = self.clipping_widget.sender()
        if radioButton.isChecked():
            clipping.lineClippingType = radioButton.selected
            line_edit.setText(radioButton.selected)

    def onClickedCurve(self, line_edit, controller):
        radioButton = self.curve_widget.sender()
        if radioButton.isChecked():
            controller.curve_type = radioButton.selected
            line_edit.setText(radioButton.selected)