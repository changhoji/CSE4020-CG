from OpenGL.GL import *
import os
import glm
import numpy as np
import ctypes

class Bvh:
    def __init__(self):
        self.root = None
        self.frame_number = None
        self.frame_time = None
        self.frames = None
        
    def set_attributes(self, root, frame_number, frame_time, frames):
        self.root = root
        self.frame_number = frame_number
        self.frame_time = frame_time
        self.frames = frames
        
    def reset_pose(self, node):
        node.joint_transform = glm.mat4()
        for child in node.children:
            self.reset_pose(child)
        
        
    def adjust_frame(self, node, frame_index, next_idx = 0):
        frame = self.frames[frame_index]
        
        if node.parent is None: # root
            translate = glm.translate((frame[0], frame[1], frame[2]))
            next_idx = 3
            R = glm.mat4()
            for i in range(len(node.channels)-3):
                chan = node.channels[3+i].upper()
                angle = glm.radians(frame[next_idx])
                axis = glm.vec3()
                if chan == 'XROTATION':
                    axis = glm.vec3(1,0,0)
                elif chan == 'YROTATION':
                    axis = glm.vec3(0,1,0)
                elif chan == 'ZROTATION':
                    axis = glm.vec3(0,0,1)
                next_idx += 1

                R = R * glm.rotate(angle, axis)
            node.joint_transform = translate * R
            node.global_transform = node.joint_transform
        
        elif node.name != 'End Site':
            R = glm.mat4()
            for i in range(len(node.channels)):
                chan = node.channels[i].upper()
                angle = glm.radians(frame[next_idx])
                axis = glm.vec3()
                if chan == 'XROTATION':
                    axis = glm.vec3(1,0,0)
                elif chan == 'YROTATION':
                    axis = glm.vec3(0,1,0)
                elif chan == 'ZROTATION':
                    axis = glm.vec3(0,0,1)
                next_idx += 1
                
                R = R * glm.rotate(angle, axis)
                
            node.joint_transform = glm.mat4(R)
            node.global_transform = node.parent.global_transform * node.parent.link_transform * node.parent.joint_transform
            
        elif node.name == 'End Site':
            node.global_transform = node.parent.global_transform * node.parent.link_transform

        a = 1
        for child in node.children:
            next_idx = self.adjust_frame(child, frame_index, next_idx)
            
        return next_idx
                
class Node:
    def __init__(self, parent, name):
        self.children = []
        self.name = name
        self.channels = []
        self.offset = None
        self.parent = parent
        
        self.line_vao = None
        self.line_cnt = 0
        self.box_vao = None
        self.box_cnt = 0
        
        self.link_transform = glm.mat4()
        self.joint_transform = glm.mat4()
        self.global_transform = glm.mat4()
        
    def append_child(self, child):
        self.children.append(child)
        
    def set_offset(self, x, y, z):
        self.offset = glm.vec3(x, y, z)
        if self.name != 'End Site':
            self.link_transform = glm.translate(self.offset)
        
    def append_channel(self, channel):
        self.channels.append(channel)
        
    def update_tree_global_transform(self):
        if self.parent is None:
            self.global_transform = glm.mat4()
        else:
            self.global_transform = self.parent.global_transform * self.parent.link_transform * self.parent.joint_transform
            
        for child in self.children:
            child.update_tree_global_transform()
    
    def prepare_line_vao(self):
        vertices = glm.array(glm.vec3(0, 0, 0), glm.vec3(1, 1, 1), 
                                   self.offset, glm.vec3(1, 1, 1),
                                   )
        
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)
        
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)
        
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6*glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(0)
        
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6*glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
        glEnableVertexAttribArray(1)
        
        self.line_vao = VAO
        self.line_cnt = len(vertices)//2
        
        for child in self.children:
            child.prepare_line_vao()
            
    def prepare_box_vao(self):
        print(self.name)
        vertices = []
        points = [glm.vec3(.1, 0, .1), glm.vec3(.1, 0, -.1), glm.vec3(-.1, 0, -.1), glm.vec3(-.1, 0, .1),
                  glm.vec3(.1, 0, .1), glm.vec3(.1, 0, -.1), glm.vec3(-.1, 0, -.1), glm.vec3(-.1, 0, .1),]
        if self.parent is not bvh.root:
            len = glm.length(self.offset)
            vec1 = glm.normalize(glm.vec3(0,len,0))
            vec2 = glm.normalize(self.offset)
            
            dot = glm.dot(vec1, vec2)
            cross = glm.cross(vec1,vec2)
            
            axis = glm.normalize(cross)
            angle = glm.acos(dot)
            
            rotate = glm.rotate(angle, axis)
            l = .05
            points = [glm.vec3(l, 0, l), glm.vec3(l, 0, -l), glm.vec3(-l, 0, -l), glm.vec3(-l, 0, l),
                      glm.vec3(l, len, l), glm.vec3(l, len, -l), glm.vec3(-l, len, -l), glm.vec3(-l, len, l),]
            points = [(rotate*glm.vec4(x, 1)).xyz for x in points]
            indices = ['012', '023', '456', '467', '015', '054', '156', '167', '267', '273', '374', '340']
            for index in indices:
                for i in index:
                    vertices.append(points[int(i)])
                    vertices.append(glm.vec3(.5, .5, 1))
            
            vertices = glm.array(np.array(vertices))
            VAO = glGenVertexArrays(1)
            glBindVertexArray(VAO)
            
            VBO = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, VBO)
            
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)
            
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6*glm.sizeof(glm.float32), None)
            glEnableVertexAttribArray(0)
            
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6*glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
            glEnableVertexAttribArray(1)
            self.box_vao = VAO
            self.box_cnt = 36
            
            
        for child in self.children:
            child.prepare_box_vao()
            
    def draw_line(self, MVP_loc, VP):
        MVP = VP * self.global_transform
        
        glBindVertexArray(self.line_vao)
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
        
        glDrawArrays(GL_LINES, 0, self.line_cnt)
        
        for child in self.children:
            child.draw_line(MVP_loc, VP)
    
    def draw_box(self, MVP_loc, VP):
        MVP = VP * self.global_transform
        
        if self.box_vao is not None:
            glBindVertexArray(self.box_vao)
            glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
            
            glDrawArrays(GL_TRIANGLES, 0, self.box_cnt)
        
        for child in self.children:
            child.draw_box(MVP_loc, VP)
        
    def print_hierarchy(self, level = 0):
        print('\t'*level + self.name + '\t' + 'link -> ')
        print(self.link_transform)
        print()
        for child in self.children:
            child.print_hierarchy(level+1)


def load_bvh_file(path):
    if os.path.splitext(path)[1] != '.bvh':
        print("can open only bvh file")
        return
    
    section = None
    root = None
    stack = []
    words = None
    
    with open(path, "r") as file:
        if section == None:
            line = file.readline().strip()
            if line == 'HIERARCHY':
                section = 'hierarchy'
            elif line == 'MOTION':
                section = 'motion'
                
        if section == 'hierarchy':
            words = file.readline().split()
            if words[0] == 'ROOT':
                root = Node(None, words[1])
            if file.readline().strip() == '{':
                stack.append(root)
                
            words = file.readline().split()
            
            while len(stack) > 0:
                
                if words[0] == 'OFFSET':
                    stack[-1].set_offset(float(words[1]), float(words[2]), float(words[3]))
                elif words[0] == '{':
                    1
                elif words[0] == 'JOINT':
                    node = Node(stack[-1], words[1])
                    stack[-1].append_child(node)
                    stack.append(node)
                elif words[0] == 'CHANNELS':
                    for i in range(int(words[1])):
                        stack[-1].append_channel(words[i+2])
                elif words[0] == '}':
                    stack.pop()
                elif words[0] == 'End':
                    end_node = Node(stack[-1], 'End Site')
                    stack[-1].append_child(end_node)
                    stack.append(end_node)
                
                words = file.readline().split()

            section = 'motion'
        
        if section == 'motion':
            words = file.readline().split()
            frame_number = int(words[1])
            words = file.readline().split()
            frame_time = float(words[2])
        
        words = file.readline().split()
        frames = []
        while len(words):
            frame = [float(num) for num in words]
            frames.append(frame)
            words = file.readline().split()
            
        bvh.set_attributes(root, frame_number, frame_time, frames)
        bvh.root.prepare_line_vao()
        bvh.root.prepare_box_vao()

            
bvh = Bvh()




