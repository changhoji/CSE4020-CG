import glm

G = 3.

def jump(time, velocity):
    period = 2 * velocity / G
    time = time % period
    
    velocity_after = velocity - G*time
    s = (velocity_after**2 - velocity**2) / -2*G
        
    return glm.translate((0, s, 0))
