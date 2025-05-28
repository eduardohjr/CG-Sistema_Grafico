from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

class FormWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GetData")
        self.setGeometry(100, 100, 300, 100)

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter the point's coordinates: ", self)
        self.layout.addWidget(self.label)

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("x,y,z")
        self.layout.addWidget(self.text_input)

        self.submit_button = QPushButton("Enviar", self)
        self.submit_button.clicked.connect(self.enviar_dados)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def enviar_dados(self):
        # Pega o texto do QLineEdit
        text = self.text_input.text()
        try :
            coordenates = tuple(map(float, coordenates.split(',')))
            if (len(coordenates) == 3):
                    return coordenates
            else:
                self.commaPopUp(1)
        except:
                self.instructionsPopUp()