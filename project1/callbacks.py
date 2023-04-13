from OpenGL.GL import *
from glfw.GLFW import *

from camera import camera

left_button_state = 0
right_button_state = 0
current_cursor = [0, 0]
diff_cursor = [0, 0]

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
    # in orthogonal, don't edit distance value
    if camera.isOrthogonal():
        return
    
    # in perspective, edit distance value for zoomming in and out
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
    
    diff_cursor = [xpos-current_cursor[0], current_cursor[1]-ypos]
    
    if left_button_state:
        camera.change_azimuth(diff_cursor[0])
        camera.change_elevation(diff_cursor[1])
    if right_button_state:
        camera.change_pan(diff_cursor[0], diff_cursor[1])
        
    current_cursor = [xpos, ypos]


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)