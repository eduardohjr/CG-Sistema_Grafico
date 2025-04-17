import sys
from window import Window
from PyQt5.QtWidgets import QApplication


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec_())