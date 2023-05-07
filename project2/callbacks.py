from OpenGL.GL import *
from glfw.GLFW import *
import glm
import os

from camera import camera
from object import *

left_button_state = 0
right_button_state = 0
current_cursor = [0, 0]
diff_cursor = [0, 0]
g_P = glm.mat4()

# glfw key callback function
def key_callback(window, key, scancode, action, mods):
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    else:
        if action==GLFW_PRESS or action==GLFW_REPEAT:
            if key == GLFW_KEY_V:
                camera.toggle_projection()
        
# glfw scroll callback function
def scroll_callback(window, xoffset, yoffset):
    # edit distance value for zoomming in and out
    if yoffset < 0:
        camera.increase_distance()
    if yoffset > 0:
        camera.decrase_distance()

# glfw button callback function
def mouse_button_callback(window, button, action, mod):
    global left_button_state, right_button_state
    
    if button==GLFW_MOUSE_BUTTON_LEFT:
        if action==GLFW_PRESS:
            left_button_state = 1
        elif action==GLFW_RELEASE:
            left_button_state = 0
    elif button==GLFW_MOUSE_BUTTON_RIGHT:
        if action==GLFW_PRESS:
            right_button_state = 1
        elif action==GLFW_RELEASE:
            right_button_state = 0
       
# glfw cursor position callback function     
def cursor_callback(window, xpos, ypos):
    global current_cursor, diff_cursor
    
    # get difference of cursor position
    diff_cursor = [xpos-current_cursor[0], current_cursor[1]-ypos]
    
    # do orbit
    if left_button_state:
        camera.change_azimuth(diff_cursor[0])
        camera.change_elevation(diff_cursor[1])
    
    #do pan
    if right_button_state:
        camera.change_pan(diff_cursor[0], diff_cursor[1])
    
    # update current cursor position
    current_cursor = [xpos, ypos]
    
def drop_callback(window, paths):
    path = paths[0]
    
    positions, normals, faces = load_obj_file(path)
    print("after load file")
    object = Object(positions, normals, faces)
                    
    print("Obj file name: " + os.path.basename(path))
    
    
def load_obj_file(path):
    if os.path.splitext(path)[1] != ".obj":
        print("can open only obj file")
        return
    
    positions = glm.array(glm.vec3(0, 0, 0))
    normals = glm.array(glm.vec3(0, 0, 0))
    faces = []
    
    with open(path, "r") as file:
        for line in file:
            args = line.split()
            
            # comment
            if len(args) == 0:
                continue
            
            if args[0] == "#":
                continue
            
            if args[0] == "v":
                pos = glm.vec3(float(args[1]), float(args[2]), float(args[3]))
                positions = positions.concat(glm.array(pos))
                
            elif args[0] == "vn":
                normal = glm.vec3(float(args[1]), float(args[2]), float(args[3]))
                normals = normals.concat(glm.array(normal))
                
            elif args[0] == "f":
                face = []
                for arg in args[1:]: # arg = 1//2
                    temp = {}
                    toks = arg.split("/") # toks = ['1', '', '2']
                    # print("toks: ", toks)
                    temp["position"] = int(toks[0])
                    temp["normal"] = 0 # temp
                    face.append(temp)
                faces.append(face)
        
    return positions, normals, faces    
