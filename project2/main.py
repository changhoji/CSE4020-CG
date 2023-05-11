from OpenGL.GL import *
from glfw.GLFW import *
import glm
import ctypes
import numpy as np
import os

from vaos import *
from callbacks import *
from shader import load_shaders
from physics import *

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

#define NLIGHT 3

in vec3 vout_surface_pos;
in vec3 vout_normal;

out vec4 FragColor;

uniform vec3 view_pos;
uniform vec3 light_pos;
uniform vec3 material_color;

vec3 calculate_shading(vec3 light_pos) {
    // light and material properties
    vec3 light_color = vec3(1,1,1);
    float material_shininess = 32.0;

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
    
    return color;
}

void main()
{
    // vec3 lights[NLIGHT] = {vec3(10, 10, 10), vec3(-10, -10, -10), vec3(0, -10, 0)};
    vec3 lights[NLIGHT];
    lights[0] = vec3(100, 100, 100);
    lights[1] = vec3(-100, 100, -100);
    lights[2] = vec3(0, -10, 0);
    vec3 result_color = calculate_shading(lights[0]);
    
    for (int i = 1; i < NLIGHT; i++) {
        vec3 color = calculate_shading(lights[i]);
        
        if (result_color.x < color.x) result_color.x = color.x;
        if (result_color.y < color.y) result_color.y = color.y;
        if (result_color.z < color.z) result_color.z = color.z;
    }
    
    
    FragColor = vec4(result_color, 1.);
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
    material_color_loc = glGetUniformLocation(shader_for_mesh, 'material_color')
    
    uniform_locs = {'M_loc':M_loc, 'material_color_loc':material_color_loc, 'MVP_loc':mesh_MVP_loc}
    
    # prepare vaos
    num_of_lines = 100
    vao_grid = prepare_vao_grid(num_of_lines)
    
    os.chdir('samples')
    path = os.path.join('cube-tri.obj')
    obj_manager.object = Object(load_object_vertices(path))
    
    obj_manager.prepare_mario_objects()
    
    # loop until the user closes the window
    while not glfwWindowShouldClose(window):     
        # enable depth test
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glClearColor(.5, .5, .5, 1.)
        glEnable(GL_DEPTH_TEST)

        glUseProgram(shader_program)

        if camera.solid:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
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
        
        # uniform eye pos
        eye = camera.get_eye_pos()
        glUniform3f(view_pos_loc, eye.x, eye.y, eye.z)
        
        # uniform light pos
        light = camera.get_light_pos(0, 0)
        glUniform3f(light_pos_loc, light.x, light.y, light.z)
        
        t = glfwGetTime()
        
        # draw objects loaded
        if obj_manager.single_mesh:
            if obj_manager.object is not None:
                obj_manager.draw_single_object(P*V, uniform_locs)
        else:
            if obj_manager.root_object is not None:
                obj_manager.root_object.set_transform(glm.translate((0, np.sin(t), 0)))
                obj_manager.objects['mario'].set_transform(jump(t,1))
                obj_manager.objects['coin'].set_transform(glm.translate((2, 0, 2))*glm.rotate(10*t, (0, 1, 0))*glm.translate((0, -np.sin(3*t)*.5, 0)))
                obj_manager.objects['tree'].set_transform(glm.translate((-2, 0, -3)))
                obj_manager.objects['wiggler'].set_transform(glm.translate((0, 0, (np.sin(2*t)))))
                obj_manager.draw_mario_objects(P*V, uniform_locs)
        
        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
