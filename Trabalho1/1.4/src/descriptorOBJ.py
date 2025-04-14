class DescriptorOBJ:
    def __init__(self, name, obj_type, color=None, filled=False):
        self.name = name
        self.type = obj_type
        self.vertices = []
        self.edges = []
        self.color = color
        self.filled = filled

    def add_vertex(self, x, y, z=0):
        self.vertices.append((x, y, z))

    def add_edge(self, v1, v2):
        self.edges.append((v1, v2))

    def add_face(self, vertices):
        """Add a face (polygon) from vertex indices"""
        for i in range(len(vertices)):
            self.add_edge(vertices[i], vertices[(i+1)%len(vertices)])

    def write_to_file(self, file):
        file.write(f"o {self.name}\n")
        file.write(f"# Type: {self.type}\n")
        
        if self.color and hasattr(self.color, 'getRgb'):
            r, g, b, _ = self.color.getRgb()
            file.write(f"usemtl {r}_{g}_{b}\n")
        
        for v in self.vertices:
            file.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        
        if self.type == "point":
            file.write(f"l 1 1\n")
        else:
            for e in self.edges:
                file.write(f"l {e[0] + 1} {e[1] + 1}\n")