from point import Point
from line import Line
from polygon import Polygon
from curve import Curve
from point3D import Point3D
from object3D import Object3D
from PyQt5.QtGui import QStandardItem, QColor
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QVBoxLayout, QTabBar, QLabel, QLineEdit, QColorDialog, QStackedWidget, QPushButton
from PyQt5.QtCore import Qt
from constants import *
from descriptorOBJ import DescriptorOBJ
from formWindow import FormWindow
import sys

class Controller():
    def __init__(self, viewport, tree):
        self.__viewport = viewport
        self.__scene = self.__viewport.scene()
        self.__tree = tree
        self.__model = self.__tree.model
        self.__current_id = 1
        self.move_multiplier = 20
        self.zoomIn_mutiplier = 1.1
        self.zoomOut_multiplier = 0.9
        self.treeIndex = 0
        self.color = None
        self.normalizedInfos = {UP: [[0, -self.move_multiplier, 0], [1, 1, 1], [0, 0, 0]],
                                DOWN: [[0, self.move_multiplier, 0], [1, 1, 1], [0, 0, 0]],
                                LEFT: [[-self.move_multiplier, 0, 0], [1, 1, 1], [0, 0, 0]],
                                RIGHT: [[self.move_multiplier, 0, 0], [1, 1, 1], [0, 0, 0]],
                                IN: [[0, 0, 0], [self.zoomIn_mutiplier]*3, [0, 0, 0]],
                                OUT: [[0, 0, 0], [self.zoomOut_multiplier]*3, [0, 0, 0]],
                                WLEFT: [[0, 0, 0], [1, 1, 1], [0, 0, -10]], 
                                WRIGHT: [[0, 0, 0], [1, 1, 1], [0, 0, 10]]   
                                }
        self.curve_type = "Bezier"


    def drawEvent(self, window, filled = False, curve=False):
        if (self.__viewport.coordenates):
            self.clearText()

            object = None

            if (len(self.__viewport.coordenates) == 1):
                object = Point(self.__viewport.coordenates.copy())
            elif (len(self.__viewport.coordenates) == 2):
                object = Line(self.__viewport.coordenates.copy())
            else:
                if (curve):
                    if (len(self.__viewport.coordenates) >= 4):
                        object = Curve(self.__viewport.coordenates.copy(), self.curve_type)
                    else:
                        self.curvePopUp()
                else:
                    object = Polygon(self.__viewport.coordenates.copy(), filled)

            if (isinstance(object, Point)):
                window.clipping.pointClippingCheck(object)
            elif (isinstance(object, Line)):
                object.draw_points = window.clipping.lineClipping(object)
            elif (isinstance(object, Polygon)):
                object.applyClipping(window.clipping)

            if (object.on_screen):
                self.__viewport.objects.append(object)
                self.color = QColorDialog().getColor()
                object.color = self.color
                object.draw(self.__viewport)
                self.addTree(object)
                self.__viewport.coordenates.clear()
            else:
                self.__viewport.coordenates.clear()
                self.offScreenPopUp()
                
    def drawPoint3DEvent(self):
        self.form_window_3D_point = QWidget()
        self.form_window_3D_point.setMinimumSize(300, 100)

        layout = QVBoxLayout()
        label = QLabel("Enter the point's coordinates: ", self.form_window_3D_point)
        layout.addWidget(label)

        
        text_input = QLineEdit(self.form_window_3D_point)
        text_input.setPlaceholderText("x,y,z")
        layout.addWidget(text_input)

        def create_point():
            self.form_window_3D_point.close()
            text = text_input.text()
            text_input.clear()

            try :
                coordenates = tuple(map(float, text.split(',')))
                if (len(coordenates) == 3):
                        obj = Point3D([coordenates])
                        self.color = QColorDialog().getColor()
                        obj.color = self.color
                        self.__viewport.objects.append(obj)
                        obj.draw(self.__viewport)
                        self.addTree(obj)
                else:
                    self.commaPopUp(3)
            except:
                self.instructionsPopUp()

        submit_button = QPushButton("Send", self.form_window_3D_point)
        submit_button.clicked.connect(create_point)
        layout.addWidget(submit_button)
        self.form_window_3D_point.setLayout(layout)

        self.form_window_3D_point.show()

    def drawObject3DEvent(self):
        self.form_window_3D_point = QWidget()
        self.form_window_3D_point.setMinimumSize(400, 200)

        layout = QVBoxLayout()
        label = QLabel("Enter the objects's coordinates: ", self.form_window_3D_point)
        layout.addWidget(label)

        example = QLabel("Ex:\n(0,0,0),(0,0,100),(0,100,0),(0,100,100),(100,0,0),(100,0,100),(100,100,0),(100,100,100)\n"
                        "(0, 1), (0, 2), (0, 4),(1, 3), (1, 5), (2, 3),(2, 6), (3, 7), (4, 5),(4, 6),(5, 7),(6, 7)\n")
        example.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(example)

        points_input = QLineEdit(self.form_window_3D_point)
        points_input.setPlaceholderText("P1, P2, ... Pn ---> Px = (x,y,z)")
        layout.addWidget(points_input)

        segments_input = QLineEdit(self.form_window_3D_point)
        segments_input.setPlaceholderText("(P1, P2), (P2, P3), ... (Pn-1, Pn) ---> ex: (0, 1), (1,2)")
        layout.addWidget(segments_input)

        def create_object():
            self.form_window_3D_point.close()
            points_tex = points_input.text()
            segments_text = segments_input.text()
            points_input.clear()

            try :
                points_values = eval(points_tex)
                segments_values = eval(segments_text)
                if (len(points_values) > 2) and (len(segments_values) > 2):
                    try:
                            points = []
                            segments = []
                            for i in range(len(points_values)):
                                x, y, z = map(float, points_values[i])
                                points.append(Point3D([(x,y,z)]))
                            for i in range(len(segments_values)):
                                p1,p2 = map(int, segments_values[i])
                                segments.append((p1,p2))
                            obj = Object3D(points, segments)
                            self.color = QColorDialog().getColor()
                            obj.color = self.color
                            self.__viewport.objects.append(obj)
                            obj.draw(self.__viewport)
                            self.addTree(obj)
                    except:
                        self.instructionsPopUp()
                else:
                    self.commaPopUp(3)
            except:
                self.instructionsPopUp()

        submit_button = QPushButton("Send", self.form_window_3D_point)
        submit_button.clicked.connect(create_object)
        layout.addWidget(submit_button)
        self.form_window_3D_point.setLayout(layout)

        self.form_window_3D_point.show()

    def clearText(self):
        for element in self.__viewport.text:
            self.__scene.removeItem(element)
        self.__viewport.text.clear()

    def clearEvent(self):
        if (not self.__viewport.objects):
            self.clearText()
            self.__viewport.coordenates.clear()
        else:
            for item in self.__viewport.objects:
                if (item.on_screen):
                    if(isinstance(item, Polygon)) or (isinstance(item, Curve)) or (isinstance(item, Object3D)):
                        for id in item.id:
                            self.__scene.removeItem(id)
                    else:
                        self.__scene.removeItem(item.id)

            self.clearText()
            self.__viewport.coordenates.clear()
            self.__viewport.objects.clear()
            self.__current_id = 1
            self.treeIndex = 0
            self.__model.removeRows(0, self.__model.rowCount())

    def upEvent(self, window):
        for object in self.__viewport.objects:
            window.normalize(object, self.normalizedInfos[UP])


    def downEvent(self, window):
        for object in self.__viewport.objects:
            window.normalize(object, self.normalizedInfos[DOWN])


    def rightEvent(self, window):
        for object in self.__viewport.objects:
            window.normalize(object, self.normalizedInfos[RIGHT])

        
    def leftEvent(self, window):
        for object in self.__viewport.objects:
            window.normalize(object, self.normalizedInfos[LEFT])


    def zoomInEvent(self, window):
        for object in self.__viewport.objects:
            window.normalize(object, self.normalizedInfos[IN])
    

    def zoomOutEvent(self, window):
        for object in self.__viewport.objects:
            window.normalize(object, self.normalizedInfos[OUT])


    def translateEvent(self, window):
        if(self.__tree.selectedIndexes()):
            index = self.__tree.selectedIndexes()[0].row()
            graphicObject = self.__viewport.objects[index]

            previous_on_screen = graphicObject.on_screen

            input = self.takeInputs(window)
            if input != None:
                graphicObject.translation(input)

            if (previous_on_screen):
                if (isinstance(graphicObject, Polygon) or isinstance(graphicObject, Curve) or isinstance(graphicObject, Object3D)):
                    for item in graphicObject.id:
                        self.__scene.removeItem(item)
                else:
                    self.__scene.removeItem(graphicObject.id)

            if (isinstance(graphicObject, Point)):
                window.normalizedWindow.clipping.pointClippingCheck(graphicObject)
            elif (isinstance(graphicObject, Line)):
                graphicObject.draw_points = window.normalizedWindow.clipping.lineClipping(graphicObject)
            else:
                graphicObject.applyClipping(window.normalizedWindow.clipping)

            if (graphicObject.on_screen):
                graphicObject.draw(self.__viewport)

            self.updateObject(graphicObject, index)

    def escalonateEvent(self, window):
        if(self.__tree.selectedIndexes()):
            index = self.__tree.selectedIndexes()[0].row()
            graphicObject =self.__viewport.objects[index]

            previous_on_screen = graphicObject.on_screen

            input = self.takeInputs(window)
            if input != None:
                graphicObject.escalonation(input)

            if (previous_on_screen):
                if (isinstance(graphicObject, Polygon) or isinstance(graphicObject, Curve) or isinstance(graphicObject, Object3D)):
                    for item in graphicObject.id:
                        self.__scene.removeItem(item)
                else:
                    self.__scene.removeItem(graphicObject.id)

            if (isinstance (graphicObject, Point)):
                window.normalizedWindow.clipping.pointClippingCheck(graphicObject)
            elif (isinstance(graphicObject, Line)):
                graphicObject.draw_points = window.normalizedWindow.clipping.lineClipping(graphicObject)
            else:
                graphicObject.applyClipping(window.normalizedWindow.clipping)

            if (graphicObject.on_screen):
                graphicObject.draw(self.__viewport)


            self.updateObject(graphicObject, index)

    def rotateObjectEvent(self, window):
        if(self.__tree.selectedIndexes()):
            index = self.__tree.selectedIndexes()[0].row()
            graphicObject = self.__viewport.objects[index]
            self.selectRotation(graphicObject, index, window)

    def addTree(self, object):
        itemID = QStandardItem("graphicObject" + str(self.__current_id))
        itemCoordenates = QStandardItem(str(object.getPoints()))
        self.__model.setItem(self.treeIndex,0, itemID)
        self.__model.setItem(self.treeIndex,1, itemCoordenates)
        self.treeIndex += 1
        self.__current_id += 1

    def updateObject(self, object, index):
        newCoordenates = object.getPoints()
        object.center = object.calculateCenter()

        result = []
        for coordenate in newCoordenates:
            result.append((float(coordenate[0]), float(coordenate[1])))
        result = QStandardItem(str(result))
        self.__model.setItem(index,1, result)

    def selectRotation(self, graphicObject, index, window):
        self.dialog = QWidget()
        self.dialog.setWindowTitle("Choice of rotation")
        self.dialog.setGeometry(100, 100, 360, 150)

        layout = QVBoxLayout()
        self.tab_bar = QTabBar()
        self.tab_bar.setShape(QTabBar.RoundedNorth)
        self.tab_content = QStackedWidget()
        self.tab_bar.addTab("")
        self.tab_bar.addTab("Center of the world")
        self.tab_bar.addTab("center of the object")
        self.tab_bar.addTab("Any point")

        self.setupTab1()
        self.rotateOnWorld(graphicObject, index, window)
        self.rotateOnCenter(graphicObject, index, window)
        self.rotateOnPoint(graphicObject, index, window)

        self.tab_bar.currentChanged.connect(self.tab_content.setCurrentIndex)
        layout.addWidget(self.tab_bar, alignment=Qt.AlignLeft)
        layout.addWidget(self.tab_content)
        self.dialog.setLayout(layout)
        self.dialog.show()

    def setupTab1(self):
        tab1_content = QLabel("Select a rotation above")
        tab1_content.setAlignment(Qt.AlignCenter)
        self.tab_content.addWidget(tab1_content)

    def rotateOnWorld(self, graphicObject, index, window):
        tab2_widget = QWidget()
        tab2_layout = QVBoxLayout()
        helper_text = QLabel("Enter the angle for the object to be rotated:")
        helper_text.setAlignment(Qt.AlignCenter)
        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("Enter the angle and axis here...")
        execute_button = QPushButton("Execute")
        execute_button.clicked.connect(lambda : self.executeRotWorld(graphicObject, index, window))
        tab2_layout.addWidget(helper_text)
        tab2_layout.addWidget(self.angle_input)
        tab2_layout.addWidget(execute_button)
        tab2_layout.setAlignment(Qt.AlignCenter)
        tab2_widget.setLayout(tab2_layout)
        self.tab_content.addWidget(tab2_widget)

    def rotateOnCenter(self, graphicObject, index, window):
        tab2_widget = QWidget()
        tab2_layout = QVBoxLayout()
        helper_text = QLabel("Enter angle for the object to be rotated:")
        helper_text.setAlignment(Qt.AlignCenter)
        self.angle_input2 = QLineEdit()
        self.angle_input2.setPlaceholderText("Enter the angle and axis here...")
        execute_button = QPushButton("Execute")
        execute_button.clicked.connect(lambda: self.executeRotCenter(graphicObject, index, window))
        tab2_layout.addWidget(helper_text)
        tab2_layout.addWidget(self.angle_input2)
        tab2_layout.addWidget(execute_button)
        tab2_layout.setAlignment(Qt.AlignCenter)
        tab2_widget.setLayout(tab2_layout)
        self.tab_content.addWidget(tab2_widget)

    def rotateOnPoint(self, graphicObject, index, window):
        tab2_widget = QWidget()
        tab2_layout = QVBoxLayout()
        helper_text = QLabel("Enter the point and angle for the object to be rotated:")
        helper_text.setAlignment(Qt.AlignCenter)
        self.angle_input3 = QLineEdit()
        self.angle_input3.setPlaceholderText("Ex: x,y,z,45,axis")
        execute_button = QPushButton("Execute")
        execute_button.clicked.connect(lambda: self.executeRotPoint(graphicObject, index, window))
        tab2_layout.addWidget(helper_text)
        tab2_layout.addWidget(self.angle_input3)
        tab2_layout.addWidget(execute_button)
        tab2_layout.setAlignment(Qt.AlignCenter)
        tab2_widget.setLayout(tab2_layout)
        self.tab_content.addWidget(tab2_widget)

    def executeRotWorld(self, object, index, window):
        previous_on_screen = object.on_screen
        try:
            angle, axis = self.angle_input.text().split(',')
            object.rotationWorld(float(angle), axis)
            self.updateObject(object, index)
            self.dialog.close()

            if (previous_on_screen):
                if (isinstance(object, Polygon) or isinstance(object, Curve) or isinstance(object, Object3D)):
                    for item in object.id:
                        self.__scene.removeItem(item)
                else:
                    self.__scene.removeItem(object.id)

            if (isinstance(object, Point)):
                window.clipping.pointClippingCheck(object)
            elif (isinstance(object,Line)):
                object.draw_points = window.clipping.lineClipping(object)
            else:
                object.applyClipping(window.clipping)

            if (object.on_screen):
                object.draw(self.__viewport)

        except:
            self.instructionsPopUp()
            return

    def executeRotCenter(self, object, index, window):
        previous_on_screen = object.on_screen
        try:
            angle, axis = self.angle_input2.text().split(',')
            object.rotationCenter(float(angle), axis)
            self.updateObject(object, index)
            self.dialog.close()

            if (previous_on_screen):
                if (isinstance(object, Polygon) or isinstance(object, Curve) or isinstance(object, Object3D)):
                    for item in object.id:
                        self.__scene.removeItem(item)
                else:
                    self.__scene.removeItem(object.id)

            if (isinstance(object, Point)):
                window.clipping.pointClippingCheck(object)
            elif (isinstance(object,Line)):
                object.draw_points = window.clipping.lineClipping(object)
            else:
                object.applyClipping(window.clipping)

            if (object.on_screen):
                object.draw(self.__viewport)
        except:
            self.instructionsPopUp()

    def executeRotPoint(self, object, index, window):
        inputs = self.angle_input3.text()
        previous_on_screen = object.on_screen
        try:
            inputs = inputs.split(',')
            values = tuple((float(value) for value in inputs[:4]))
            angle = values[3]
            points = [values[i] for i in range(0,3)]
            axis = inputs[4]
            if (len(inputs) == 5):
                object.rotationPoint(angle, points, axis)
                self.updateObject(object, index)
                self.dialog.close()


                if (previous_on_screen):
                    if (isinstance(object, Polygon) or isinstance(object, Curve) or isinstance(object, Object3D)):
                        for item in object.id:
                            self.__scene.removeItem(item)
                    else:
                        self.__scene.removeItem(object.id)

                if (isinstance(object, Point)):
                    window.clipping.pointClippingCheck(object)
                elif (isinstance(object,Line)):
                    object.draw_points = window.clipping.lineClipping(object)
                else:
                    object.applyClipping(window.clipping)


                if (object.on_screen):
                    object.draw(self.__viewport)

            else:
                self.commaPopUp(2)
        except:
            self.instructionsPopUp()
        

    def takeInputs(self, window):
        coordenates, done = QInputDialog.getText(
            window, 'Input Dialog', 'Give points like this -> x,y,z :') 

        if done :
            try:
                coordenates = tuple(map(float, coordenates.split(',')))
                if (len(coordenates) == 3):
                    return coordenates
                else:
                    self.commaPopUp(1)
            except:
                self.instructionsPopUp()
            
    def instructionsPopUp(self):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR")
        msg.setText("ERROR! Please follow the instructions")
        msg.setIcon(QMessageBox.Warning)

        x = msg.exec_()

    def commaPopUp(self, type):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR")
        if type == 1:
            msg.setText("Give only one coordenate (x,y) \n"
                        "Use '.' to separate fractional numbers")
        elif type == 2:
            msg.setText("Give only one coordenate (x,y) and one angle (n)\n"
                        "Use '.' to separate fractional numbers")
        elif type == 3:
            msg.setText("Give only one coordenate (x,y,z)\n"
                        "Use '.' to separate fractional numbers")
            
        msg.setIcon(QMessageBox.Question)
        x = msg.exec_()

    def offScreenPopUp(self):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR")
        msg.setText("ERROR! Slect a point inside the red react")
        msg.setIcon(QMessageBox.Warning)

        x = msg.exec_()

    def curvePopUp(self):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR")
        msg.setText("Give at least 4 points")
        msg.setIcon(QMessageBox.Warning)   

        x = msg.exec_()     

    def rotateWindowLeft(self, window):
        for object in self.__viewport.objects:
            window.normalize(object, self.normalizedInfos[WLEFT])


    def rotateWindowRight(self, window):
        for object in self.__viewport.objects:
            window.normalize(object, self.normalizedInfos[WRIGHT])

    def saveToObj(self, filename, index=None):
        base_filename = filename[:-4] if filename.endswith('.obj') else filename
        mtl_filename = f"{base_filename}.mtl"
        
        with open(mtl_filename, 'w') as mtl_file:
            mtl_file.write("# Material file\n")
            if index is not None:
                obj = self.__viewport.objects[index]
                if obj.color and hasattr(obj.color, 'getRgb'):
                    r, g, b, _ = obj.color.getRgb()
                    color_key = f"{r}_{g}_{b}"
                    mtl_file.write(f"newmtl {color_key}\n")
                    mtl_file.write(f"Kd {r/255:.3f} {g/255:.3f} {b/255:.3f}\n")
            else:
                color_set = set()
                for obj in self.__viewport.objects:
                    if obj.color and hasattr(obj.color, 'getRgb'):
                        r, g, b, _ = obj.color.getRgb()
                        color_key = f"{r}_{g}_{b}"
                        if color_key not in color_set:
                            color_set.add(color_key)
                            mtl_file.write(f"newmtl {color_key}\n")
                            mtl_file.write(f"Kd {r/255:.3f} {g/255:.3f} {b/255:.3f}\n")

        with open(filename, 'w') as file:
            file.write("# Wavefront OBJ file\n")
            file.write("# Generated by CG-Sistema_Grafico\n")
            file.write(f"mtllib {mtl_filename.split('/')[-1]}\n\n")
            
            if index is not None:
                obj = self.__viewport.objects[index]
                obj_type = "point" if isinstance(obj, Point) else \
                        "point3d" if isinstance(obj, Point3D) else \
                        "object3d" if isinstance(obj, Object3D) else \
                        "line" if isinstance(obj, Line) else \
                        "polygon" if isinstance(obj, Polygon) else \
                        obj.type 
                
                if obj_type == "polygon":
                    fill_status = "filled" if obj.filled else "unfilled"
                    clip_status = "clipped" if hasattr(obj, 'clipped_points') and obj.clipped_points != obj.points else "unclipped"
                    file.write(f"# Fill: {fill_status}\n")
                    file.write(f"# Clipping: {clip_status}\n")
                
                descritor = DescriptorOBJ(f"obj_{index}", obj_type, obj.color, getattr(obj, 'filled', False))
                if isinstance(obj, Point3D):
                    x, y, z = obj.points[0]
                    descritor.add_vertex(x, y, z)
                    descritor.add_edge(0, 0)
                elif isinstance(obj, Object3D):
                    for point in obj.points:
                        x, y, z = point.points[0]
                        descritor.add_vertex(x, y, z)
                    for edge in obj.segments:
                        descritor.add_edge(edge[0], edge[1])
                else:
                    if isinstance(obj, Point3D):
                        x, y, z = obj.points[0]                
                        descritor.add_vertex(x, y, z)
                    else:
                        for point in obj.points:
                            descritor.add_vertex(point[0], point[1], point[2] if len(point) > 2 else 0)
                    if obj_type == "point":
                        descritor.add_edge(0, 0)
                    elif obj_type == "line":
                        descritor.add_edge(0, 1)
                    else:
                        descritor.add_face(range(len(obj.points)))
                
                descritor.write_to_file(file)
            else:
                for idx, obj in enumerate(self.__viewport.objects):
                    obj_type = "point" if isinstance(obj, Point) else \
                        "point3d" if isinstance(obj, Point3D) else \
                        "object3d" if isinstance(obj, Object3D) else \
                        "line" if isinstance(obj, Line) else \
                        "polygon" if isinstance(obj, Polygon) else \
                        obj.type 
                    
                    if obj_type == "polygon":
                        fill_status = "filled" if obj.filled else "unfilled"
                        clip_status = "clipped" if hasattr(obj, 'clipped_points') and obj.clipped_points != obj.points else "unclipped"
                        file.write(f"# Fill: {fill_status}\n")
                        file.write(f"# Clipping: {clip_status}\n")
                    
                    descritor = DescriptorOBJ(f"obj_{idx}", obj_type, obj.color, getattr(obj, 'filled', False))
                    if isinstance(obj, Point3D):
                        x, y, z = obj.points[0]
                        descritor.add_vertex(x, y, z)
                        descritor.add_edge(0, 0)
                    elif isinstance(obj, Object3D):
                        for point in obj.points:
                            x, y, z = point.points[0]
                            descritor.add_vertex(x, y, z)
                        for edge in obj.segments:
                            descritor.add_edge(edge[0], edge[1])
                    else:
                        if isinstance(obj, Point3D):
                            x, y, z = obj.points[0]                
                            descritor.add_vertex(x, y, z)
                        else:
                            for point in obj.points:
                                descritor.add_vertex(point[0], point[1], point[2] if len(point) > 2 else 0)
                        if obj_type == "point":
                            descritor.add_edge(0, 0)
                        elif obj_type == "line":
                            descritor.add_edge(0, 1)
                        else:
                            descritor.add_face(range(len(obj.points)))

                    
                    descritor.write_to_file(file)
                    file.write("\n")

    def loadFromObj(self, filename):
        try:
            base_filename = filename[:-4] if filename.endswith('.obj') else filename
            mtl_filename = f"{base_filename}.mtl"
            colors = {}
            
            try:
                with open(mtl_filename, 'r') as mtl_file:
                    current_mtl = None
                    for line in mtl_file:
                        line = line.strip()
                        if line.startswith('newmtl '):
                            current_mtl = line[7:]
                        elif line.startswith('Kd') and current_mtl:
                            try:
                                parts = line.split()
                                r = float(parts[1]) * 255
                                g = float(parts[2]) * 255
                                b = float(parts[3]) * 255
                                colors[current_mtl] = QColor(int(r), int(g), int(b))
                            except (IndexError, ValueError):
                                continue
            except FileNotFoundError:
                pass
                
            with open(filename, 'r') as file:
                current_vertices = []
                current_edges = []
                current_filled = False
                self.current_color = None
                window = self.__viewport.parent()
                obj_type = ''

                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                        
                    if line.startswith('#'):
                        if 'Type: polygon' in line:
                            obj_type = 'polygon'
                        elif 'Type: curve' in line:
                            obj_type = 'curve'
                        elif 'Type: point' in line and 'Type: point3d' not in line:
                            obj_type = 'point'
                        elif 'Type: line' in line:
                            obj_type = 'line'
                        elif 'Type: Bezier' in line:
                            obj_type = 'Bezier'
                        elif 'Type: BSpline' in line:
                            obj_type = 'BSpline'
                        elif 'Type: point3d' in line:
                            obj_type = 'point3d'
                        elif 'Type: object3d' in line:
                            obj_type = 'object3d'
                        elif 'Fill: filled' in line:
                            current_filled = True
                        elif 'Fill: unfilled' in line:
                            current_filled = False
                        continue

                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    
                    if parts[0] == 'v':
                        try:
                            x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                            if obj_type in ['point3d', 'object3d']:
                                current_vertices.append((x, y, z))
                            else:
                                current_vertices.append((x, y))
                        except (IndexError, ValueError):
                            continue
                            
                    elif parts[0] == 'l' and current_vertices:
                        try:
                            v1, v2 = int(parts[1])-1, int(parts[2])-1
                            if 0 <= v1 < len(current_vertices) and 0 <= v2 < len(current_vertices):
                                current_edges.append((v1, v2))
                        except (IndexError, ValueError):
                            continue
                    
                    elif parts[0] == 'usemtl':
                        try:
                            color_key = parts[1]
                            if color_key in colors:
                                self.current_color = colors[color_key]
                        except (IndexError, ValueError):
                            continue
                    
                    if (parts[0] == 'o' or not line) and current_vertices:
                        print(f"Creating object with type: {obj_type}")
                        obj = self._create_object_from_data(current_vertices, current_edges, obj_type, current_filled)
                        obj_type = ''

                        if isinstance(obj, Point):
                            window.normalizedWindow.clipping.pointClippingCheck(obj)
                            obj.draw(self.__viewport)
                        elif isinstance(obj, Line):
                            obj.draw_points = window.normalizedWindow.clipping.lineClipping(obj)
                            obj.draw(self.__viewport)
                        elif (isinstance(obj, Polygon) or isinstance(obj, Curve)):
                            obj.applyClipping(window.normalizedWindow.clipping)
                            obj.draw(self.__viewport)
                        elif (isinstance(obj, Object3D)):
                            obj.applyClipping(window.normalizedWindow.clipping)
                            obj.draw(self.__viewport)
                        elif (isinstance(obj, Point3D)):
                            window.normalizedWindow.clipping.pointClippingCheck(obj)
                            obj.draw(self.__viewport)
                        
                        
                        current_vertices = []
                        current_edges = []
                        current_filled = False
                        self.current_color = None
                        obj_type = ''

                if current_vertices:
                    obj = self._create_object_from_data(current_vertices, current_edges, obj_type, current_filled)
                    print(f"Creating object with type: {obj_type}")
                    if isinstance(obj, Point) and obj_type == 'point':
                        window.normalizedWindow.clipping.pointClippingCheck(obj)
                        obj.draw(self.__viewport)
                    elif isinstance(obj, Line):
                        obj.draw_points = window.normalizedWindow.clipping.lineClipping(obj)
                        obj.draw(self.__viewport)
                    elif (isinstance(obj, Polygon) or isinstance(obj, Curve)):
                        obj.applyClipping(window.normalizedWindow.clipping)
                        obj.draw(self.__viewport)
                    elif (isinstance(obj, Object3D)):
                            obj.applyClipping(window.normalizedWindow.clipping)
                            obj.draw(self.__viewport)
                    elif (isinstance(obj, Point3D)):
                        window.normalizedWindow.clipping.pointClippingCheck(obj)
                        obj.draw(self.__viewport)
                        
                    
            self.__viewport.update()
                        
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to load file: {str(e)}")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            
    def _create_object_from_data(self, vertices, edges, obj_type, filled=False):
        obj = None
        if obj_type == 'point':
            obj = Point([vertices[0]])
        elif obj_type == 'point3d':
            obj = Point3D([vertices[0]])
        elif obj_type == 'object3d':
            points = [Point3D([v]) for v in vertices]
            obj = Object3D(points, edges)
        elif obj_type == 'line':
            obj = Line([vertices[0], vertices[1]])
        elif obj_type == 'polygon':
            obj = Polygon(vertices, filled=filled)
        else:
            obj = Curve(vertices, obj_type)

        if obj and self.current_color:
            obj.color = self.current_color
            
        if obj:
            self.__viewport.objects.append(obj)
            self.addTree(obj)
        return obj
