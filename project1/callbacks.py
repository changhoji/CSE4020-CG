from glfw.GLFW import *
import glm
import numpy as np

left_button_state = 0
right_button_state = 0
current_cursor = [0, 0]
diff_cursor = [0, 0]

g_cam_ang = 0.
g_cam_height = .1
g_translate = glm.vec3(0., 0., 0.)
g_zoom = 1.
g_pan = glm.vec3(0., 0., 0.)

def key_callback(window, key, scancode, action, mods):
    global g_cam_ang, g_cam_height, g_translate
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    else:
        if action==GLFW_PRESS or action==GLFW_REPEAT:
            if key==GLFW_KEY_1:
                g_cam_ang += np.radians(-10)
            elif key==GLFW_KEY_3:
                g_cam_ang += np.radians(10)
            elif key==GLFW_KEY_2:
                g_cam_height += .05
            elif key==GLFW_KEY_W:
                g_cam_height += -.05
                
            elif key==GLFW_KEY_Q:
                g_translate.x += .1
            elif key==GLFW_KEY_A:
                g_translate.x += -.1
            elif key==GLFW_KEY_E:
                g_translate.y += .1
            elif key==GLFW_KEY_D:
                g_translate.y += -.1
            elif key==GLFW_KEY_Z:
                g_translate.z += .1
            elif key==GLFW_KEY_X:
                g_translate.z += -.1
                
def scroll_callback(window, xoffset, yoffset):
    global g_zoom
    if yoffset < 0:
        g_zoom = max(g_zoom-.1, .1)
    if yoffset > 0:
        g_zoom += .1 

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
            
def cursor_callback(window, xpos, ypos):
    global current_cursor, diff_cursor, g_pan
    
    diff_cursor = [xpos-current_cursor[0], current_cursor[1]-ypos]
    
    if right_button_state:
        g_pan = glm.vec3(g_pan.x, g_pan.y+diff_cursor[1], g_pan.z)
        print(g_pan)
    
    current_cursor = [xpos, ypos]