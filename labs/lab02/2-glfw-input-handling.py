from OpenGL.GL import *
from glfw.GLFW import *

# key callback 생성
def key_callback(window, key, scancode, action, mods):
    # esc 누르면 종료시킴
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
        return
    
    # 키 누를때 메시지 출력
    elif key!=GLFW_KEY_SPACE:
        if action==GLFW_PRESS:
            print("press %c" %key)
        elif action==GLFW_RELEASE:
            print("release %c" %key)
        elif action==GLFW_REPEAT:
            print("repeat %c" %key)
            
    # 스페이스바 누르면 커서 위치를 출력
    elif key==GLFW_KEY_SPACE and action==GLFW_PRESS:
        print("press space: (%d, %d)" %glfwGetCursorPos(window))

# cursor callback 생성
def cursor_callback(window, xpos, ypos):
    # cursor event가 발생하면 cursor 위치를 출력해줌
    print("mouse cursor moving: (%d, %d)" %(xpos, ypos))
    
# button callback 생성
def button_callback(window, button, action, mod):
    if button==GLFW_MOUSE_BUTTON_LEFT:
        if action==GLFW_PRESS:
            print("press left mouse button: (%d %d)" %glfwGetCursorPos(window))
        elif action==GLFW_REPEAT:
            print("repeat left mouse button: (%d, %d)" %glfwGetCursorPos(window))
        elif action==GLFW_RELEASE:
            print("release left mouse button: (%d, %d)" %glfwGetCursorPos(window))
    elif button==GLFW_MOUSE_BUTTON_RIGHT:
        if action==GLFW_PRESS:
            print("press right mouse button: (%d %d)" %glfwGetCursorPos(window))
        elif action==GLFW_REPEAT:
            print("repeat right mouse button: (%d, %d)" %glfwGetCursorPos(window))
        elif action==GLFW_RELEASE:
            print("release right mouse button: (%d, %d)" %glfwGetCursorPos(window))
        
            
# scroll callback 생성
def scroll_callback(window, xoffset, yoffset):
    print("mouse wheel scroll: %d, %d" %(xoffset, yoffset))
    
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
    
    # callback 함수들 지정해줌
    glfwSetKeyCallback(window, key_callback)
    glfwSetCursorPosCallback(window, cursor_callback)
    glfwSetMouseButtonCallback(window, button_callback)
    glfwSetScrollCallback(window, scroll_callback)
    
    # shouldClose일 때까지 반복해서 창을 띄움
    while not glfwWindowShouldClose(window):
        glfwSwapBuffers(window)
        glfwPollEvents()
    
    # while 끝나면 종료시키기
    glfwTerminate()
    
if __name__ == "__main__":
    main()