from OpenGL.GL import *
from glfw.GLFW import *
import glm

g_vertex_shader_src = '''
#version 330 core

layout (location = 0) in vec3 vin_pos;
layout (location = 1) in vec3 vin_color;

out vec4 vout_color;

uniform float u_variable;

void main() {
    gl_Position = vec4(vin_pos.x + u_variable, vin_pos.y, vin_pos.z, 1.0);
    
    vout_color = vec4(vin_color*((u_variable+1)/2), 1);
}
'''

g_fragment_shader_src = '''
#version 330 core

in vec4 vout_color;

out vec4 FragColor;

void main() {
    FragColor = vout_color;
}
'''

def load_shaders(vertex_shader_source, fragment_shader_source):
    # build and compile our shader program
    # ------------------------------------
    
    # vertex shader 
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)    # create an empty shader object
    glShaderSource(vertex_shader, vertex_shader_source) # provide shader source code
    glCompileShader(vertex_shader)                      # compile the shader object
    
    # check for shader compile errors
    success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
    if (not success):
        infoLog = glGetShaderInfoLog(vertex_shader)
        print("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" + infoLog.decode())
        
    # fragment shader
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)    # create an empty shader object
    glShaderSource(fragment_shader, fragment_shader_source) # provide shader source code
    glCompileShader(fragment_shader)                        # compile the shader object
    
    # check for shader compile errors
    success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
    if (not success):
        infoLog = glGetShaderInfoLog(fragment_shader)
        print("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" + infoLog.decode())

    # link shaders
    shader_program = glCreateProgram()               # create an empty program object
    glAttachShader(shader_program, vertex_shader)    # attach the shader objects to the program object
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)                    # link the program object

    # check for linking errors
    success = glGetProgramiv(shader_program, GL_LINK_STATUS)
    if (not success):
        infoLog = glGetProgramInfoLog(shader_program)
        print("ERROR::SHADER::PROGRAM::LINKING_FAILED\n" + infoLog.decode())
        
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program    # return the shader program

# key_callback 함수를 만들어둠
def key_callback(window, key, scancode, action, mods):
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
        
def main():
    if not glfwInit():
        return
    
    # opengl 3.3 사용
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    
    # legacy opengl 사용하지 않음
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
    
    window = glfwCreateWindow(800, 800, "2021035487", None, None)
    if not window:
        glfwTerminate()
        return
    
    glfwMakeContextCurrent(window)
    
    # keyCallBack 지정해줌
    glfwSetKeyCallback(window, key_callback)
    
    
    # shader program 지정
    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)
    glUseProgram(shader_program)
    
    # uniform 설정
    u_variable_loc = glGetUniformLocation(shader_program, "u_variable")
    
    # vertices 지정
    vertices = glm.array(glm.float32, 
                              # color 설정해줌!
            -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
             0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
             0.0,  0.5, 0.0,  0.0, 0.0, 1.0,
        )
    
    # VAO 만들고 지정
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    
    # VBO 만들고 지정
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)
    
    # 간격을 6으로 조정해줌
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6*glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)
    
    # layout = 1이므로 layout = 0에서 3개를 받아온 뒤에 3개를 layout = 1로 집어넣음! (간격은 6으로)
    # 이때 마지막 parameter인 pointer는 처음 3개를 받아온 다음에 봐야하기 때문에 3으로! (이때 void pointer로 넘겨야 함)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6*glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1);
    
    # shouldClose일 때까지 반복해서 창을 띄움
    while not glfwWindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT)
        
        
        glBindVertexArray(VAO)
        
        t = glfwGetTime()
        temp = glm.sin(t)
        
        glUniform1f(u_variable_loc, temp)
        
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        glfwSwapBuffers(window)
        glfwPollEvents()
    
    # while 끝나면 종료시키기
    glfwTerminate()
    
if __name__ == "__main__":
    main()
    
    
