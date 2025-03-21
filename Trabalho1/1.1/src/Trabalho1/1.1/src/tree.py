from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QTreeView, QAbstractItemView, QScrollBar, QHeaderView
from PyQt5.QtCore import Qt

class Tree(QTreeView):
    def __init__(self, parent):
        QTreeView.__init__(self, parent)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Id", "Coordenates"])
        self.setModel(self.model)

        self.setVerticalScrollBar(QScrollBar(Qt.Vertical, self))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.setHorizontalScrollBar(QScrollBar(Qt.Horizontal, self))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.header().setMinimumSectionSize(70)


