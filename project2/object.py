from OpenGL.GL import *
from glfw.GLFW import *
import numpy as np
import glm
import os

class ObjectManager:
    def __init__(self):
        self.object = None
        self.root_object = None
        self.single_mesh = True
        
    def set_object(self, object):
        self.object = object

    def set_root_object(self, object):
        self.root_object = object
        
    def draw_single_object(self, VP, locs):
        self.object.update_tree_global_transform()
        self.object.draw_object(VP, locs)
        
    def prepare_mario_objects(self):
        os.chdir('hierarchical')
        path = os.path.join('hemisphere.obj')
        
        ground = Object(load_object_vertices(path), None, glm.translate((0, 2, 0))*glm.scale((8, 5, 8)), glm.vec3(.8, .8, 1))
        mario = Object(load_object_vertices(os.path.join('mario.obj')), ground, glm.translate((0, 2, 0))*glm.scale((.2, .2, .2)), glm.vec3(.7, .3, .3))
        coin = Object(load_object_vertices(os.path.join('coin.obj')), ground, glm.translate((0, 3, 0))*glm.scale((.005, .005, .005)), glm.vec3(1, 1, 0))
        tree = Object(load_object_vertices(os.path.join('tree.obj')), ground, glm.translate((0, 2, 0))*glm.scale((.01, .01, .01)), glm.vec3(.2, 1, .2))
        
        self.root_object = ground
        
    def draw_mario_objects(self, VP, locs):
        self.root_object.update_tree_global_transform()
        self.root_object.draw_objects(VP, locs)        
        
class Object:       
    def __init__(self, vertices, parent=None, shape_transform=glm.mat4(), color=glm.vec3(.7,.7,.7)):
        self.vao, self.cnt = self.prepare_vao(vertices)
        
        # hierarchy
        self.parent = parent
        self.children = []
        if parent is not None:
            parent.children.append(self)

        # transform
        self.transform = glm.mat4()
        self.global_transform = glm.mat4()

        # shape
        self.shape_transform = shape_transform
        self.color = color

    def set_transform(self, transform):
        self.transform = transform

    def update_tree_global_transform(self):
        if self.parent is not None:
            self.global_transform = self.parent.get_global_transform() * self.transform
        else:
            self.global_transform = self.transform

        for child in self.children:
            child.update_tree_global_transform()

    def get_global_transform(self):
        return self.global_transform
    def get_shape_transform(self):
        return self.shape_transform
    def get_color(self):
        return self.color

    def draw_object(self, VP, uniform_locs):
        M = self.global_transform * self.shape_transform
        MVP = VP*M
        
        color = self.get_color()
        
        glBindVertexArray(self.vao)
        glUniformMatrix4fv(uniform_locs['M_loc'], 1, GL_FALSE, glm.value_ptr(M))
        glUniformMatrix4fv(uniform_locs['MVP_loc'], 1, GL_FALSE, glm.value_ptr(MVP))
        glUniform3f(uniform_locs['material_color_loc'], color.r, color.g, color.b)
        glDrawArrays(GL_TRIANGLES, 0, self.cnt)
        
    def draw_objects(self, VP, uniform_locs):
        MVP = VP*self.global_transform*self.shape_transform
        color = self.color
        
        glBindVertexArray(self.vao)
        glUniformMatrix4fv(uniform_locs['MVP_loc'], 1, GL_FALSE, glm.value_ptr(MVP))
        glUniform3f(uniform_locs['material_color_loc'], color.r, color.g, color.b)
        glDrawArrays(GL_TRIANGLES, 0, self.cnt)
        
        for child in self.children:
            child.draw_objects(VP, uniform_locs)
        
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
        
def load_object_vertices(path):
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
    
    return vertices
        
obj_manager = ObjectManager()
