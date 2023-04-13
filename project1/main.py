from OpenGL.GL import *
from glfw.GLFW import *
import glm
import ctypes
import numpy as np

from vaos import *
from callbacks import *
from shader import load_shaders

from camera import camera




# vertex shader source code
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

# fragment shader source code
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
    
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback)

    # load shaders
    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)

    # get uniform locations
    MVP_loc = glGetUniformLocation(shader_program, 'MVP')
    
    num_of_lines = 20
    # prepare vaos
    vao_ground_lines = prepare_vao_ground_lines(num_of_lines)
    vao_triangle = prepare_vao_triangle()
    vao_frame = prepare_vao_frame()
    vao_cube = prepare_vao_cube()
    
    # loop until the user closes the window
    while not glfwWindowShouldClose(window):     
        # enable depth test
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        glUseProgram(shader_program)

        # -- draw in world frame --

        # projection matrix
        P = camera.get_projection_matrix()
        # view matrix
        V = camera.get_view_matrix()
        # M in world frame
        I = glm.mat4()
        
        # get MVP matrix
        MVP = P*V*I
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))

        # draw lines in xz plane
        glBindVertexArray(vao_ground_lines)
        glDrawArrays(GL_LINES, 0, num_of_lines*8+4)
        
        glBindVertexArray(vao_frame)
        glDrawArrays(GL_LINES, 0, 6)
        
        # -- draw in world frame --
        
        
        # -- draw objects --
        
        # get M matrix
        th = np.radians(glfwGetTime()*90)
        R = glm.rotate(th, glm.vec3(0,0,1))
        
        MVP = P*V*R
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
        
        glBindVertexArray(vao_triangle)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        # draw_cube_array(vao_cube, MVP, MVP_loc)
        
        # -- draw object --
        
        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
