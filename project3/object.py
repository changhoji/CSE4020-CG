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
        self.sum = 0
        self.max_level = 0 
        
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
        self.level = None
        
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
    
    def update_level(self, level):
        if self.level is None:
            self.level = level
        else:
            self.level = min(self.level, level)
        
        bvh.max_level = max(bvh.max_level, self.level)
        
        if self.parent is not None:
            self.parent.update_level(level+1)
        
        
    def update_tree_global_transform(self):
        if self.parent is None:
            self.global_transform = glm.mat4()
        else:
            self.global_transform = self.parent.global_transform * self.parent.link_transform * self.parent.joint_transform
            
        for child in self.children:
            child.update_tree_global_transform()
    
    def prepare_line_vao(self):
        vertices = glm.array(glm.vec3(0, 0, 0), glm.vec3(.9, 1,.3), 
                                   self.offset, glm.vec3(.9, 1, .3),
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
        vertices = []
        
        if self.parent is not bvh.root:
            len = glm.length(self.offset)
            vec1 = glm.normalize(glm.vec3(0,len,0))
            vec2 = glm.normalize(self.offset)
            
            dot = glm.dot(vec1, vec2)
            cross = glm.cross(vec1,vec2)
            
            axis = glm.normalize(cross)
            angle = glm.acos(dot)
            
            rotate = glm.rotate(angle, axis)
            points = [glm.vec3(bvh.sum, 0, bvh.sum), glm.vec3(bvh.sum, 0, -bvh.sum), glm.vec3(-bvh.sum, 0, -bvh.sum), glm.vec3(-bvh.sum, 0, bvh.sum),
                      glm.vec3(bvh.sum, len, bvh.sum), glm.vec3(bvh.sum, len, -bvh.sum), glm.vec3(-bvh.sum, len, -bvh.sum), glm.vec3(-bvh.sum, len, bvh.sum),]
            points = [(rotate*glm.vec4(x, 1)).xyz for x in points]
            indices = ['021', '032', '456', '467', '015', '054', '165', '126', '276', '237', '347', '304']
            
            for index in indices:
                v1 = points[int(index[1])] - points[int(index[0])]
                v2 = points[int(index[2])] - points[int(index[0])]
                normal = glm.normalize(glm.cross(v1, v2))
                for i in index:
                    vertices.append(points[int(i)])
                    vertices.append(normal)
            
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
    
    def draw_box(self, VP, uniform_locs):
        MVP = VP * self.global_transform
        if self.box_vao is not None and self.level <= bvh.max_level-1:
            glBindVertexArray(self.box_vao)
            glUniformMatrix4fv(uniform_locs['MVP'], 1, GL_FALSE, glm.value_ptr(MVP))
            glUniformMatrix4fv(uniform_locs['M'], 1, GL_FALSE, glm.value_ptr(self.global_transform))
            
            glDrawArrays(GL_TRIANGLES, 0, self.box_cnt)
        
        for child in self.children:
            child.draw_box(VP, uniform_locs)
        
    def print_hierarchy(self, level = 0):
        print('\t'*level + self.name)
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
    bvh.sum = 0
    num_of_joint = 0
    
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
                    bvh.sum += glm.length(stack[-1].offset)*.0075
                elif words[0] == '{':
                    1
                elif words[0] == 'JOINT':
                    node = Node(stack[-1], words[1])
                    stack[-1].append_child(node)
                    stack.append(node)
                    num_of_joint += 1
                elif words[0] == 'CHANNELS':
                    for i in range(int(words[1])):
                        stack[-1].append_channel(words[i+2])
                elif words[0] == '}':
                    # if stack[-1].name != 'End Site' and len(stack[-1].children) == 0:
                    #     node = Node(stack[-1], 'End Site')
                    #     temp = stack[-1].offset
                    #     temp *= .3
                    #     node.set_offset(temp.x, temp.y, temp.z)
                    #     stack[-1].append_child(node)
                    #     node.update_level(0)
                    stack.pop()
                elif words[0] == 'End':
                    end_node = Node(stack[-1], 'End Site')
                    stack[-1].append_child(end_node)
                    stack.append(end_node)
                    end_node.update_level(0)
                    num_of_joint += 1
                
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
    
        print(f'file name: {os.path.basename(path)}')
        print(f'number of frames: {bvh.frame_number}')
        print(f'FPS: {1/bvh.frame_time}')
        print(f'number of joints: {num_of_joint}')
        print('all joint names: ')
        bvh.root.print_hierarchy()

            
bvh = Bvh()




