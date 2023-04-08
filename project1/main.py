from OpenGL.GL import *
from glfw.GLFW import *
import glm
import ctypes
import numpy as np

from shader import load_shaders
# from callbacks import *
from VAOs.ground_lines import *
from VAOs.triangle import *

# from glfw.GLFW import *
# import glm
# import numpy as np

left_button_state = 0
right_button_state = 0
current_cursor = [0, 0]
diff_cursor = [0, 0]

g_cam_ang = 0.
g_cam_ang2 = glm.degrees(45.)
g_cam_height = .1
g_translate = glm.vec3(0., 0., 0.)
g_zoom = .1
g_pan = glm.vec3(0., 0., 0.)
g_distance = 1

dr = 0

P = [glm.ortho(-1,1,-1,1,-1,10), glm.perspective(glm.radians(90.), 1, .01, 1000)]
P_index = 0

def prepare_vao_frame():
    # prepare vertex data (in main memory)
    vertices = glm.array(glm.float32,
        # position        # color
         0.0, 0.0, 0.0,  1.0, 0.0, 0.0, # x-axis start
         1.0, 0.0, 0.0,  1.0, 0.0, 0.0, # x-axis end 
         0.0, 0.0, 0.0,  0.0, 1.0, 0.0, # y-axis start
         0.0, 1.0, 0.0,  0.0, 1.0, 0.0, # y-axis end 
         0.0, 0.0, 0.0,  0.0, 0.0, 1.0, # z-axis start
         0.0, 0.0, 1.0,  0.0, 0.0, 1.0, # z-axis end 
    )

    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex colors
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO

def key_callback(window, key, scancode, action, mods):
    global g_cam_ang, g_cam_height, g_translate, right_button_state, P_index
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
        
        if key == GLFW_KEY_V and action == GLFW_PRESS:
            P_index = (P_index + 1) % 2
                    
        
                
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
    global current_cursor, diff_cursor, g_pan, g_cam_ang, g_cam_ang2, dr
    
    diff_cursor = [xpos-current_cursor[0], current_cursor[1]-ypos]
    
    if left_button_state:
        g_cam_ang += diff_cursor[0]*.01
        g_cam_ang2 += diff_cursor[1]*.01
    if right_button_state:
        dr = diff_cursor[0]*.001
        g_pan = g_pan + glm.vec3(5*dr*np.cos(-g_cam_ang), diff_cursor[1]*.01, 5*dr*np.sin(-g_cam_ang))
    
    current_cursor = [xpos, ypos]


g_vertex_shader_src = '''
#version 330 core

layout (location = 0) in vec3 vin_pos; 
layout (location = 1) in vec3 vin_color; 

out vec4 vout_color;

uniform mat4 MVP;

void main()
{
    // 3D points in homogeneous coordinates
    vec4 p3D_in_hcoord = vec4(vin_pos.xyz, 1.0);

    gl_Position = MVP * p3D_in_hcoord;

    vout_color = vec4(vin_color, 1.);
}
'''

g_fragment_shader_src = '''
#version 330 core

in vec4 vout_color;

out vec4 FragColor;

void main()
{
    FragColor = vout_color;
}
'''



def main():
    # initialize glfw
    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)   # OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)  # Do not allow legacy OpenGl API calls
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE) # for macOS

    # create a window and OpenGL context
    window = glfwCreateWindow(800, 800, '2021035487', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)

    # register event callbacks
    glfwSetKeyCallback(window, key_callback);
    glfwSetScrollCallback(window, scroll_callback)
    glfwSetCursorPosCallback(window, cursor_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)

    # load shaders
    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)

    # get uniform locations
    MVP_loc = glGetUniformLocation(shader_program, 'MVP')
    
    # prepare vaos
    vao_ground_lines = prepare_vao_ground_lines()
    vao_triangle = prepare_vao_triangle()
    vao_frame = prepare_vao_frame()

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):
        # render
        
        # enable depth test (we'll see details later)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        glUseProgram(shader_program)

        # projection matrix
        up_vec = glm.vec3(0, 1, 0)
        if (np.sin(g_cam_ang2) < 0):
            up_vec = glm.vec3(0, -1, 0)
        
        # view matrix
        V = glm.lookAt(glm.vec3(.1*np.sin(g_cam_ang)*np.sin(g_cam_ang2),.1*np.cos(g_cam_ang2),.1*np.cos(g_cam_ang)*np.sin(g_cam_ang2))+g_pan
                       , glm.vec3(0,0,0)+g_pan, up_vec)*glm.scale(glm.mat4(), glm.vec3(1., 1., 1.)*g_zoom)
        
        # current frame: P*V*I (now this is the world frame)
        I = glm.mat4()
        
        # get MVP matrix
        MVP = P[P_index]*V*I
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))

        # draw lines in xz plane
        glBindVertexArray(vao_ground_lines)
        glDrawArrays(GL_LINES, 0, num_of_lines*8+4)
        
        glBindVertexArray(vao_frame)
        glDrawArrays(GL_LINES, 0, 6)
        
        
        
        t = glfwGetTime()

        # rotation
        th = np.radians(t*90)
        R = glm.rotate(th, glm.vec3(0,0,1))
        MVP = P[P_index]*V*R
        
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
        
        glBindVertexArray(vao_triangle)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()