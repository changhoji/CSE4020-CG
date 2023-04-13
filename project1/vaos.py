from OpenGL.GL import *
from glfw.GLFW import *
import glm



def prepare_vao_cube():
    # prepare vertex data (in main memory)
    # 36 vertices for 12 triangles
    vertices = glm.array(glm.float32,
        # position            color
        -0.5 ,  0.5 ,  0.5 ,  1, 1, 1, # v0
         0.5 , -0.5 ,  0.5 ,  1, 1, 1, # v2
         0.5 ,  0.5 ,  0.5 ,  1, 1, 1, # v1
                    
        -0.5 ,  0.5 ,  0.5 ,  1, 1, 1, # v0
        -0.5 , -0.5 ,  0.5 ,  1, 1, 1, # v3
         0.5 , -0.5 ,  0.5 ,  1, 1, 1, # v2
                    
        -0.5 ,  0.5 , -0.5 ,  1, 1, 1, # v4
         0.5 ,  0.5 , -0.5 ,  1, 1, 1, # v5
         0.5 , -0.5 , -0.5 ,  1, 1, 1, # v6
                    
        -0.5 ,  0.5 , -0.5 ,  1, 1, 1, # v4
         0.5 , -0.5 , -0.5 ,  1, 1, 1, # v6
        -0.5 , -0.5 , -0.5 ,  1, 1, 1, # v7
                    
        -0.5 ,  0.5 ,  0.5 ,  1, 1, 1, # v0
         0.5 ,  0.5 ,  0.5 ,  1, 1, 1, # v1
         0.5 ,  0.5 , -0.5 ,  1, 1, 1, # v5
                    
        -0.5 ,  0.5 ,  0.5 ,  1, 1, 1, # v0
         0.5 ,  0.5 , -0.5 ,  1, 1, 1, # v5
        -0.5 ,  0.5 , -0.5 ,  1, 1, 1, # v4
 
        -0.5 , -0.5 ,  0.5 ,  1, 1, 1, # v3
         0.5 , -0.5 , -0.5 ,  1, 1, 1, # v6
         0.5 , -0.5 ,  0.5 ,  1, 1, 1, # v2
                    
        -0.5 , -0.5 ,  0.5 ,  1, 1, 1, # v3
        -0.5 , -0.5 , -0.5 ,  1, 1, 1, # v7
         0.5 , -0.5 , -0.5 ,  1, 1, 1, # v6
                    
         0.5 ,  0.5 ,  0.5 ,  1, 1, 1, # v1
         0.5 , -0.5 ,  0.5 ,  1, 1, 1, # v2
         0.5 , -0.5 , -0.5 ,  1, 1, 1, # v6
                    
         0.5 ,  0.5 ,  0.5 ,  1, 1, 1, # v1
         0.5 , -0.5 , -0.5 ,  1, 1, 1, # v6
         0.5 ,  0.5 , -0.5 ,  1, 1, 1, # v5
                    
        -0.5 ,  0.5 ,  0.5 ,  1, 1, 1, # v0
        -0.5 , -0.5 , -0.5 ,  1, 1, 1, # v7
        -0.5 , -0.5 ,  0.5 ,  1, 1, 1, # v3
                    
        -0.5 ,  0.5 ,  0.5 ,  1, 1, 1, # v0
        -0.5 ,  0.5 , -0.5 ,  1, 1, 1, # v4
        -0.5 , -0.5 , -0.5 ,  1, 1, 1, # v7
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

def draw_cube_array(vao, MVP, MVP_loc):
    glBindVertexArray(vao)
    for i in range(5):
        for j in range(5):
            for k in range(5):
                MVP_cube = MVP * glm.translate(glm.vec3(1*i, 1*j, 1*k)) * glm.scale(glm.vec3(.5,.5,.5))
                glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP_cube))
                glDrawArrays(GL_TRIANGLES, 0, 36)

def prepare_vao_frame():
    # prepare vertex data (in main memory)
    vertices = glm.array(glm.float32,
        # position        # color
         0.0, 0.0, 0.0,  1.0, 0.0, 0.0, # x-axis start
         10.0, 0.0, 0.0,  1.0, 0.0, 0.0, # x-axis end 
         0.0, 0.0, 0.0,  0.0, 1.0, 0.0, # y-axis start
         0.0, 10.0, 0.0,  0.0, 1.0, 0.0, # y-axis end 
         0.0, 0.0, 0.0,  0.0, 0.0, 1.0, # z-axis start
         0.0, 0.0, 10.0,  0.0, 0.0, 1.0, # z-axis end 
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

# num_of_lines: parameter of number of lines in ground (=20: drawn from (-20, 20) to (20, 20) in xz plane)
def prepare_vao_ground_lines(num_of_lines):
    # initialize vertices array
    vertices = glm.array(glm.float32)
    
    for i in range(-num_of_lines, num_of_lines+1):
        color = 0.5 if (i%5) else 1.0 # highlight in every 5 stride
        i = float(i)
        
        temp = glm.array(glm.float32,   
            # lines parallel to x-axis
            -num_of_lines, 0.0, i, color, color, color,
             num_of_lines, 0.0, i, color, color, color,
            
            # lines parralel to z-axis
            i, 0.0, -num_of_lines, color, color, color,
            i, 0.0,  num_of_lines, color, color, color,
        )
        vertices = vertices.concat(temp) # append

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

def prepare_vao_triangle():
    # prepare vertex data (in main memory)
    vertices = glm.array(glm.float32,
        # position        # color
         0., 0.0, 0.0,  1.0, 0.0, 0.0, # v0
         1., 0.0, 0.0,  0.0, 1.0, 0.0, # v1
         0.0, 1., 0.0,  0.0, 0.0, 1.0, # v2
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