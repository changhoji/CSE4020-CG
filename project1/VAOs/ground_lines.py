from OpenGL.GL import *
import glm
import numpy as np
import ctypes

num_of_lines = 10

def prepare_vao_ground_lines():
    # prepare vertex data (in main memory)
    vertices = glm.array(glm.float32)
    
    for i in range(-num_of_lines, num_of_lines+1):
        color = 0.5 if (i%5) else 1.0
        i = float(i)
        
        temp = glm.array(glm.float32,                         
            -10.0, 0.0, i, color, color, color,
             10.0, 0.0, i, color, color, color,
            
            i, 0.0, -10.0, color, color, color,
            i, 0.0,  10.0, color, color, color,
        )
        vertices = vertices.concat(temp)      

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

