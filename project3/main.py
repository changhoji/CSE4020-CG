from OpenGL.GL import *
from glfw.GLFW import *
import glm
import ctypes
import numpy as np
import os
import time

from vaos import *
from callbacks import *
from shader import *

from camera import camera
from object import *
from mode import modes


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
    shader_normal = load_shaders(g_vertex_shader_normal_src, g_fragment_shader_normal_src)

    # get uniform locations
    MVP_loc = glGetUniformLocation(shader_program, 'MVP')
    MVP_normal_loc = glGetUniformLocation(shader_normal, 'MVP')
    M_normal_loc = glGetUniformLocation(shader_normal, 'M')
    view_pos_loc = glGetUniformLocation(shader_normal, 'view_pos')
    
    # prepare vaos
    num_of_lines = 100
    vao_grid = prepare_vao_grid(num_of_lines)
    
    path = os.path.join("samples/jump-twist.bvh")
    path = os.path.join("samples/sample-walk.bvh")
    # path = os.path.join("samples/sample-spin.bvh")
    # path = os.path.join("samples/jumping.bvh")
    # path = os.path.join("samples/side-step.bvh")..
    load_bvh_file(path)
    
    bvh.root.print_hierarchy()
    
    
    toggle = 0
    curtime = time.time()
    frame_index = 0
    
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
        glDrawArrays(GL_LINES, 0, num_of_lines*8+4+6)
        
        
        if bvh.root is not None:
            # draw bvh objects
            if modes.animating is True:
                if toggle == 1:
                    if time.time() - curtime > bvh.frame_time:
                        if frame_index < bvh.frame_number:
                            curtime = time.time()
                            bvh.adjust_frame(bvh.root, frame_index)
                            frame_index += 1
                            if frame_index == bvh.frame_number:
                                frame_index = 0
                else:
                    frame_index = 0
                    toggle = 1
            elif modes.animating is False:
                bvh.reset_pose(bvh.root)
                toggle = 0
            
            bvh.root.update_tree_global_transform()
            
            if modes.line is True:
                bvh.root.draw_line(MVP_loc, P*V)
            else:
                glUseProgram(shader_normal)
                bvh.root.draw_box(MVP_normal_loc, M_normal_loc, view_pos_loc, P*V, camera.get_eye_pos())
        
        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
