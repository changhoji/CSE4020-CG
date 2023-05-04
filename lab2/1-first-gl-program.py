from OpenGL.GL import *
from glfw.GLFW import *

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
    
    window = glfwCreateWindow(800, 800, "first-gl-program", None, None)
    if not window:
        glfwTerminate()
        return
    
    glfwMakeContextCurrent(window)
    
    # keyCallBack 지정해줌
    glfwSetKeyCallback(window, key_callback)
    
    # shouldClose일 때까지 반복해서 창을 띄움
    while not glfwWindowShouldClose(window):
        glfwSwapBuffers(window)
        glfwPollEvents()
    
    # while 끝나면 종료시키기
    glfwTerminate()
    
if __name__ == "__main__":
    main()