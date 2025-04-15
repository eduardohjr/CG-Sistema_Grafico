from graphicObject import Point, Line, Polygon
from PyQt5.QtGui import QStandardItem, QColor
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QVBoxLayout, QTabBar, QLabel, QLineEdit, QColorDialog, QStackedWidget, QPushButton
from PyQt5.QtCore import Qt
from constants import *
from descriptorOBJ import DescriptorOBJ

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
        self.normalizedInfos = {UP: [[0,self.move_multiplier], [1,1], 0],
                                DOWN: [[0,-self.move_multiplier], [1,1],0],
                                LEFT: [[-self.move_multiplier,0], [1,1],0],
                                RIGHT: [[self.move_multiplier,0], [1,1],0],
                                IN: [[0,0], [self.zoomIn_mutiplier, self.zoomIn_mutiplier], 0],
                                OUT: [[0,0], [self.zoomOut_multiplier, self.zoomOut_multiplier], 0],
                                WLEFT: [[0,0], [1,1], -10],
                                WRIGHT: [[0,0], [1,1], 10]
                                }


    def drawEvent(self, window, filled = False):
        if (self.__viewport.coordenates):
            self.clearText()

            object = None

            if (len(self.__viewport.coordenates) == 1):
                object = Point(self.__viewport.coordenates.copy())
            elif (len(self.__viewport.coordenates) == 2):
                object = Line(self.__viewport.coordenates.copy())
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
                    if(isinstance(item, Polygon)):
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
            graphicObject.translation(input)

            if (previous_on_screen):
                if (isinstance(graphicObject, Polygon)):
                    for item in graphicObject.id:
                        self.__scene.removeItem(item)
                else:
                    self.__scene.removeItem(graphicObject.id)

            if (isinstance(graphicObject, Point)):
                window.normalizedWindow.clipping.pointClippingCheck(graphicObject)
            elif (isinstance(graphicObject, Line)):
                graphicObject.draw_points = window.normalizedWindow.clipping.lineClipping(graphicObject)
            elif (isinstance(graphicObject, Polygon)):
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
            graphicObject.escalonation(input)

            if (previous_on_screen):
                if (isinstance(graphicObject, Polygon)):
                    for item in graphicObject.id:
                        self.__scene.removeItem(item)
                else:
                    self.__scene.removeItem(graphicObject.id)

            if (isinstance (graphicObject, Point)):
                window.normalizedWindow.clipping.pointClippingCheck(graphicObject)
            elif (isinstance(graphicObject, Line)):
                graphicObject.draw_points = window.normalizedWindow.clipping.lineClipping(graphicObject)

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
        self.angle_input.setPlaceholderText("Enter the angle here...")
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
        self.angle_input2.setPlaceholderText("Enter the angle here...")
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
        self.angle_input3.setPlaceholderText("Ex: x,y,45")
        execute_button = QPushButton("Execute")
        execute_button.clicked.connect(lambda: self.executeRotPoint(graphicObject, index, window))
        tab2_layout.addWidget(helper_text)
        tab2_layout.addWidget(self.angle_input3)
        tab2_layout.addWidget(execute_button)
        tab2_layout.setAlignment(Qt.AlignCenter)
        tab2_widget.setLayout(tab2_layout)
        self.tab_content.addWidget(tab2_widget)

    def executeRotWorld(self, object, index, window):
        angle = self.angle_input.text()
        previous_on_screen = object.on_screen
        try:
            object.rotationWord(float(angle))
            self.updateObject(object, index)
            self.dialog.close()

            if (previous_on_screen):
                if (isinstance(object, Polygon)):
                    for item in object.id:
                        self.__scene.removeItem(item)
                else:
                    self.__scene.removeItem(object.id)

            if (isinstance(object, Point)):
                window.clipping.pointClippingCheck(object)
            elif (isinstance(object,Line)):
                object.draw_points = window.clipping.lineClipping(object)

            if (object.on_screen):
                object.draw(self.__viewport)

        except:
            self.instructionsPopUp()
            return

    def executeRotCenter(self, object, index, window):
        angle = self.angle_input2.text()
        previous_on_screen = object.on_screen
        try:
            object.rotationCenter(float(angle))
            self.updateObject(object, index)
            self.dialog.close()

            if (previous_on_screen):
                if (isinstance(object, Polygon)):
                    for item in object.id:
                        self.__scene.removeItem(item)
                else:
                    self.__scene.removeItem(object.id)

            if (isinstance(object, Point)):
                window.clipping.pointClippingCheck(object)
            elif (isinstance(object,Line)):
                object.draw_points = window.clipping.lineClipping(object)

            if (object.on_screen):
                object.draw(self.__viewport)
        except:
            self.instructionsPopUp()

    def executeRotPoint(self, object, index, window):
        inputs = self.angle_input3.text()
        previous_on_screen = object.on_screen
        try:
            inputs = tuple(map(float, inputs.split(',')))
            angle = inputs[2]
            points = [inputs[i] for i in range(0,2)]
            if (len(inputs) == 3):
                object.rotationPoint(angle, points)
                self.updateObject(object, index)
                self.dialog.close()


                if (previous_on_screen):
                    if (isinstance(object, Polygon)):
                        for item in object.id:
                            self.__scene.removeItem(item)
                    else:
                        self.__scene.removeItem(object.id)

                if (isinstance(object, Point)):
                    window.clipping.pointClippingCheck(object)
                elif (isinstance(object,Line)):
                    object.draw_points = window.clipping.lineClipping(object)


                if (object.on_screen):
                    object.draw(self.__viewport)

            else:
                self.commaPopUp(2)
        except:
            self.instructionsPopUp()
        

    def takeInputs(self, window):
        coordenates, done = QInputDialog.getText(
            window, 'Input Dialog', 'Give points like this -> x,y :') 

        if done :
            try:
                coordenates = tuple(map(float, coordenates.split(',')))
                if (len(coordenates) == 2):
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
            
        msg.setIcon(QMessageBox.Question)
        x = msg.exec_()

    def offScreenPopUp(self):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR")
        msg.setText("ERROR! Slect a point inside the red react")
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
                obj_type = "point" if len(obj.points) == 1 else \
                        "line" if len(obj.points) == 2 else \
                        "polygon"
                
                # Add fill status and clipping info for polygons
                if obj_type == "polygon":
                    fill_status = "filled" if obj.filled else "unfilled"
                    clip_status = "clipped" if hasattr(obj, 'clipped_points') and obj.clipped_points != obj.points else "unclipped"
                    file.write(f"# Fill: {fill_status}\n")
                    file.write(f"# Clipping: {clip_status}\n")
                
                descritor = DescriptorOBJ(f"obj_{index}", obj_type, obj.color, getattr(obj, 'filled', False))
                for point in obj.points:
                    descritor.add_vertex(point[0], point[1], 0)
                
                if obj_type == "point":
                    descritor.add_edge(0, 0)
                elif obj_type == "line":
                    descritor.add_edge(0, 1)
                else:
                    descritor.add_face(range(len(obj.points)))
                
                descritor.write_to_file(file)
            else:
                for idx, obj in enumerate(self.__viewport.objects):
                    obj_type = "point" if len(obj.points) == 1 else \
                            "line" if len(obj.points) == 2 else \
                            "polygon"
                    
                    # Add fill status and clipping info for polygons
                    if obj_type == "polygon":
                        fill_status = "filled" if obj.filled else "unfilled"
                        clip_status = "clipped" if hasattr(obj, 'clipped_points') and obj.clipped_points != obj.points else "unclipped"
                        file.write(f"# Fill: {fill_status}\n")
                        file.write(f"# Clipping: {clip_status}\n")
                    
                    descritor = DescriptorOBJ(f"obj_{idx}", obj_type, obj.color, getattr(obj, 'filled', False))
                    for point in obj.points:
                        descritor.add_vertex(point[0], point[1], 0)
                    
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
                
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        if line.startswith('# Fill: filled'):
                            current_filled = True
                        elif line.startswith('# Fill: unfilled'):
                            current_filled = False
                        continue
                        
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                        
                    if parts[0] == 'v':
                        try:
                            x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
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
                        obj = self._create_object_from_data(current_vertices, current_edges, current_filled)
                        
                        # Apply proper clipping based on object type
                        if isinstance(obj, Point):
                            window.normalizedWindow.clipping.pointClippingCheck(obj)
                            if obj.on_screen:
                                obj.draw(self.__viewport)
                        elif isinstance(obj, Line):
                            obj.draw_points = window.normalizedWindow.clipping.lineClipping(obj)
                            if obj.on_screen:
                                obj.draw(self.__viewport)
                        elif isinstance(obj, Polygon):
                            obj.applyClipping(window.normalizedWindow.clipping)
                            if obj.on_screen:
                                obj.draw(self.__viewport)
                        
                        current_vertices = []
                        current_edges = []
                        current_filled = False
                        self.current_color = None
                        
                if current_vertices:
                    obj = self._create_object_from_data(current_vertices, current_edges, current_filled)
                    if isinstance(obj, Point):
                        window.normalizedWindow.clipping.pointClippingCheck(obj)
                        if obj.on_screen:
                            obj.draw(self.__viewport)
                    elif isinstance(obj, Line):
                        obj.draw_points = window.normalizedWindow.clipping.lineClipping(obj)
                        if obj.on_screen:
                            obj.draw(self.__viewport)
                    elif isinstance(obj, Polygon):
                        obj.applyClipping(window.normalizedWindow.clipping)
                        if obj.on_screen:
                            obj.draw(self.__viewport)
                    
            self.__viewport.update()
                        
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to load file: {str(e)}")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            
    def _create_object_from_data(self, vertices, edges, filled=False):
        if len(vertices) == 1:
            obj = Point([vertices[0]])
        elif len(vertices) == 2:
            obj = Line([vertices[0], vertices[1]])
        else:
            obj = Polygon(vertices, filled=filled)
            
        if self.current_color:
            obj.color = self.current_color
            
        self.__viewport.objects.append(obj)
        self.addTree(obj)
        return obj
    

    
    
