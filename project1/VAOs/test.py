import glm

a = glm.array(glm.float32(1), glm.float32(2))
b = glm.array(glm.float32, 3, 4)
a.concat(b)
print(a)

import glm

num_of_lines = 5

vertices = glm.array(glm.float32)
for i in range(-num_of_lines, num_of_lines+1):
    color = 0.8 if (i%5) else 1.0
    i = float(i)
    
    temp = glm.array(glm.float32,                         
        -10.0, 0.0, i, color, color, color,
            10.0, 0.0, i, color, color, color,
        
        i, 0.0, -10.0, color, color, color,
        i, 0.0,  10.0, color, color, color
    )
    vertices.concat(temp)
    
print(vertices)