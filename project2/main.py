from OpenGL.GL import *
from glfw.GLFW import *
import glm
import ctypes
import numpy as np
import os

from vaos import *
from callbacks import *
from shader import load_shaders

from camera import camera
from object import obj_manager

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

out vec3 vout_surface_pos;
out vec3 vout_normal;

uniform mat4 mesh_MVP;
uniform mat4 M;

void main()
{
    vec4 p3D_in_hcoord = vec4(vin_pos.xyz, 1.0);
    gl_Position = mesh_MVP * p3D_in_hcoord;

    vout_surface_pos = vec3(M * vec4(vin_pos, 1));
    vout_normal = normalize( mat3(inverse(transpose(M)) ) * vin_normal);
}
'''

g_fragment_shader_src_mesh = '''
#version 330 core

in vec3 vout_surface_pos;
in vec3 vout_normal;

out vec4 FragColor;

uniform vec3 view_pos;
uniform vec3 light_pos;

void main()
{
    // light and material properties
    // vec3 light_pos = vec3(100, 100, 100);
    vec3 light_color = vec3(1,1,1);
    vec3 material_color = vec3(69,30,20)*0.004;
    float material_shininess = 100.0;

    // light components
    vec3 light_ambient = 0.1*light_color;
    vec3 light_diffuse = light_color;
    vec3 light_specular = light_color;

    // material components
    vec3 material_ambient = material_color;
    vec3 material_diffuse = material_color;
    vec3 material_specular = light_color;  // for non-metal material

    // ambient
    vec3 ambient = light_ambient * material_ambient;

    // for diffiuse and specular
    vec3 normal = normalize(vout_normal);
    vec3 surface_pos = vout_surface_pos;
    vec3 light_dir = normalize(light_pos - surface_pos);

    // diffuse
    float diff = max(dot(normal, light_dir), 0);
    vec3 diffuse = diff * light_diffuse * material_diffuse;

    // specular
    vec3 view_dir = normalize(view_pos - surface_pos);
    vec3 reflect_dir = reflect(-light_dir, normal);
    float spec = pow( max(dot(view_dir, reflect_dir), 0.0), material_shininess);
    vec3 specular = spec * light_specular * material_specular;

    vec3 color = ambient + diffuse + specular;
    FragColor = vec4(color, 1.);
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
    shader_for_mesh = load_shaders(g_vertex_shader_src_mesh, g_fragment_shader_src_mesh)

    # get uniform locations
    MVP_loc = glGetUniformLocation(shader_program, 'MVP')
    mesh_MVP_loc = glGetUniformLocation(shader_for_mesh, 'mesh_MVP')
    view_pos_loc = glGetUniformLocation(shader_for_mesh, 'view_pos')
    M_loc = glGetUniformLocation(shader_for_mesh, 'M')
    light_pos_loc = glGetUniformLocation(shader_for_mesh, 'light_pos')
    
    # prepare vaos
    num_of_lines = 100
    vao_grid = prepare_vao_grid(num_of_lines)
    
    os.chdir('samples')
    path = os.path.join('cube-tri.obj')
    obj_manager.object = load_object(path)
    
    # loop until the user closes the window
    while not glfwWindowShouldClose(window):     
        # enable depth test
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glClearColor(.5, .5, .5, 1.)
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
        
        M = glm.translate((0, 1, 0))
        MVP = P*V*M
        eye = camera.get_eye_pos()
        glUseProgram(shader_for_mesh)
        glUniformMatrix4fv(mesh_MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
        glUniformMatrix4fv(M_loc, 1, GL_FALSE, glm.value_ptr(M))
        glUniform3f(view_pos_loc, eye.x, eye.y, eye.z)
        eye = camera.get_light_pos(np.radians(10), 0)
        glUniform3f(light_pos_loc, eye.x, eye.y, eye.z)
        
        if obj_manager.single_mesh:
            if obj_manager.object is not None:
                glBindVertexArray(obj_manager.object.vao)
                glDrawArrays(GL_TRIANGLES, 0, obj_manager.object.cnt)
        else:
            draw_mario_objects()
        
        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
