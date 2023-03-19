# Lab02

## Assignment

### 명세

빨간색의 정사각형 그리기

### 해결

3-hello-triangle.py에서 일부분만 변경함

우선 정점을 아래와 같이 설정해 주고

```python
vertices = glm.array(glm.float32,
            -0.5, -0.5, 0.0,
            -0.5,  0.5, 0.0,
             0.5,  0.5, 0.0,
             0.5, -0.5, 0.0
        )
```

아래와 같이 4개의 정점을 사용해 triangle_fan을 draw하도록 변경

```python
glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
```
