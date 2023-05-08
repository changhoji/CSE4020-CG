from OpenGL.GL import *
from glfw.GLFW import *
import numpy as np
import glm

class ObjectManager:
    def __init__(self):
        self.object = None
        self.vao = None
        self.exist = False
        self.cnt = 0
        
    def set_object(self, object):
        self.object = object
        self.vao, self.cnt = object.prepare_vao()
        self.exist = True

class Object:
    def __init__(self, positions, normals, faces):
        self.positions = positions 
        self.normals = normals
        self.faces = faces
        object_manager.set_object(self)
        
    def prepare_vao(self):
        # temp vec3
        vertices = []
        
        for index, face in enumerate(self.faces):
            # if index%1000 == 0:
            #     print("f:"+str(index+1)+"/"+str(len(self.faces)))
            for i in range(1, len(face) - 2 + 1, 1):
                vertices.append(self.positions[face[0]["position"]])
                vertices.append(self.normals[face[0]["normal"]])
                for j in range(2):
                    pos_index = face[i+j]["position"]
                    normal_index = face[i+j]["normal"]
                    vertices.append(self.positions[pos_index])
                    vertices.append(self.normals[normal_index])
                    
        # delete temp vec3
        
        vertices = glm.array(np.array(vertices))
        
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
        
object_manager = ObjectManager()