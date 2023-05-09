from OpenGL.GL import *
from glfw.GLFW import *
import numpy as np
import glm
import os

class ObjectManager:
    def __init__(self):
        self.object = None
        self.objects = []
        self.single_mesh = True
        
    def set_object(self, object):
        self.object = object

    
        
class Object:
    def __init__(self, vertices):
        self.vao, self.cnt = self.prepare_vao(vertices)
        
    def prepare_vao(self, vertices):
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)
        
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)
        
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6*glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(0)
        
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_TRUE, 6*glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
        glEnableVertexAttribArray(1)
        
        return VAO, int(len(vertices)/2)
        
def load_object(path):
    if os.path.splitext(path)[1] != ".obj":
        print("can open only obj file")
        return
    
    print("path: ", path)
    
    positions = []
    normals = []
    
    vertices = []
    
    with open(path, "r") as file:
        for line in file:
            args = line.split()
            
            # comment
            if len(args) == 0:
                continue
            
            if args[0] == "#":
                continue
            
            if args[0] == "v":
                positions.append(glm.vec3(float(args[1]), float(args[2]), float(args[3])))
                
            elif args[0] == "vn":
                normals.append(glm.vec3(float(args[1]), float(args[2]), float(args[3])))
                
            elif args[0] == "f":
                face = []
                for arg in args[1:]: # arg = 1//2
                    temp = {}
                    toks = arg.split("/") # toks = ['1', '', '2']
                    # print("toks: ", toks)
                    temp["position"] = int(toks[0])-1
                    temp["normal"] = int(toks[2])-1 # normal이 다 0,0,0 이었음
                    face.append(temp)
                for i in range(1, len(face) - 1):
                    vertices.append(positions[face[0]["position"]])
                    vertices.append(normals[face[0]["normal"]])
                    for j in range(2):
                        pos_index = face[i+j]["position"]
                        normal_index = face[i+j]["normal"]
                        vertices.append(positions[pos_index])
                        vertices.append(normals[normal_index])
        
    vertices = glm.array(np.array(vertices))
    
    return Object(vertices)
        
def prepare_mario_objects():
        os.chdir('samples/hierarchical')
        path = os.path.join('hemisphere.obj')
        load_object(path)
    
def draw_mario_objects():
    1

obj_manager = ObjectManager()

