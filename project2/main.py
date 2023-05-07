from OpenGL.GL import *
from glfw.GLFW import *
import glm
import ctypes
import numpy as np

from vaos import *
from callbacks import *
from shader import load_shaders

from camera import camera
from object import object_manager

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

g_vertex_shader_src_mesh = '''
#version 330 core

layout (location = 0) in vec3 vin_pos; 
layout (location = 1) in vec3 vin_normal; 

out vec4 vout_color;

uniform mat4 mesh_MVP;

void main()
{
    // 3D points in homogeneous coordinates
    vec4 p3D_in_hcoord = vec4(vin_pos.xyz, 1.0);

    gl_Position = mesh_MVP * p3D_in_hcoord;

    vout_color = vec4(.7, .7, .7, 1.);
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
    glfwSetDropCallback(window, drop_callback)

    # load shaders.
    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)
    shader_for_mesh = load_shaders(g_vertex_shader_src_mesh, g_fragment_shader_src)

    # get uniform locations
    MVP_loc = glGetUniformLocation(shader_program, 'MVP')
    mesh_MVP_loc = glGetUniformLocation(shader_for_mesh, 'mesh_MVP')
    
    # prepare vaos
    num_of_lines = 100
    vao_grid = prepare_vao_grid(num_of_lines)
    
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
        glBindVertexArray(vao_grid)
        glDrawArrays(GL_LINES, 0, num_of_lines*8+4)
        
        # -- draw objects --
        glUseProgram(shader_for_mesh)
        glUniformMatrix4fv(mesh_MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
        
        if object_manager.exist == True:
            glBindVertexArray(object_manager.vao)
            glDrawArrays(GL_TRIANGLES, 0, object_manager.cnt)
        
        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
