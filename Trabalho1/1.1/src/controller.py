
from graphicObject import Point, Line, Polygon
from  PyQt5 import QtGui


class Controller():
    def __init__(self, viewport):
        self.__viewport = viewport
        self.__current_id = 1
        self.zoomIn_mutiplier = 1.1
        self.zoomOut_multiplier = 0.9

    def drawEvent(self):
        for element in self.__viewport.text:
            self.__viewport.scene().removeItem(element)

        if (len(self.__viewport.coordenates) == 0):
            print("Nenhum ponto selecionado")

        elif (len(self.__viewport.coordenates) == 1):
            point = Point(self.__viewport.coordenates, self.__current_id)
            self.__current_id += 1
            self.__viewport.objects.append(point)
            point.draw(self.__viewport)

            self.__viewport.coordenates.clear()

        elif (len(self.__viewport.coordenates) == 2):
            line = Line(self.__viewport.coordenates, self.__current_id)
            self.__current_id += 1
            self.__viewport.objects.append(line)
            line.draw(self.__viewport)

            self.__viewport.coordenates.clear()
        
        else:
            polygon = Polygon(self.__viewport.coordenates, self.__current_id)
            self.__current_id += 1
            self.__viewport.objects.append(polygon)
            polygon.draw(self.__viewport)

            self.__viewport.coordenates.clear()

    def clearEvent(self):
        self.__viewport.scene().clear()
        self.__current_id = 1

    def zoomInEvent(self):
        pass
