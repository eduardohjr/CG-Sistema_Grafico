import sys
from window import Window
from PyQt5.QtWidgets import QApplication


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec_())

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt


class Perspective3DWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projeção Perspectiva (modelo USP)")
        self.setGeometry(100, 100, 600, 600)

        # Distância do plano de projeção (d)
        self.d = 5.0

        # Ângulos para rotação
        self.angle_x = 0
        self.angle_y = 0

        # Controle mouse
        self.last_mouse_pos = None

        # Vértices do cubo
        self.vertices = np.array([
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1]
        ])

        # Arestas do cubo
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

    def rotate(self, vertex):
        x, y, z = vertex
        # Rotação em X
        cos_x = np.cos(self.angle_x)
        sin_x = np.sin(self.angle_x)
        y_new = y * cos_x - z * sin_x
        z_new = y * sin_x + z * cos_x

        # Rotação em Y
        cos_y = np.cos(self.angle_y)
        sin_y = np.sin(self.angle_y)
        x_new = x * cos_y + z_new * sin_y
        z_final = -x * sin_y + z_new * cos_y

        return np.array([x_new, y_new, z_final])

    def perspective_projection(self, x, y, z):
        """
        Projeção perspectiva segundo o site USP:
        x' = d*x / (z + d)
        y' = d*y / (z + d)
        Para garantir que (z + d) > 0, o cubo precisa estar atrás da câmera (z > -d).
        """
        z_offset = z + self.d
        if z_offset == 0:
            z_offset = 0.0001  # evita divisão por zero

        xp = self.d * x / z_offset
        yp = self.d * y / z_offset
        return xp, yp

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        cx = self.width() // 2
        cy = self.height() // 2

        projected_points = []
        for v in self.vertices:
            rotated = self.rotate(v)
            xp, yp = self.perspective_projection(*rotated)

            scale = 150  # escala para ajustar tamanho na tela
            x2d = int(cx + xp * scale)
            y2d = int(cy - yp * scale)  # eixo y invertido na tela
            projected_points.append((x2d, y2d))

        for edge in self.edges:
            p1 = projected_points[edge[0]]
            p2 = projected_points[edge[1]]
            painter.drawLine(p1[0], p1[1], p2[0], p2[1])

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_mouse_pos is not None:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()

            self.angle_y += dx * 0.01
            self.angle_x += dy * 0.01

            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = None

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.d -= delta * 0.3
        if self.d < 0.1:
            self.d = 0.1  # evita que d fique negativo ou zero
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Perspective3DWidget()
    window.show()
    sys.exit(app.exec_())