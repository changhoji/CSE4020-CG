import glm
import numpy as np

class Camera:
    def __init__(self):
        self.distance  = 10.
        self.azimuth   = glm.degrees(30.)
        self.elevation = glm.degrees(45.)
        self.pan = glm.vec3(0.,0.,0.)  
        self.perspective = True
                  
    def get_orbit(self):
        return glm.vec3(
            np.cos(self.azimuth)*np.cos(self.elevation),
            np.sin(self.elevation),
            np.sin(self.azimuth)*np.cos(self.elevation)
        )
        
    def increase_distance(self):
        self.distance *= 1.1
    def decrase_distance(self):
        self.distance = max(.001, self.distance*.9)
        
    def change_azimuth(self, diff):
        self.azimuth += diff*glm.degrees(.0005)
    def change_elevation(self, diff):
        self.elevation += diff*glm.degrees(.0005)
        
    def change_pan(self, dxz, dy):
        self.pan += glm.vec3(
            dxz*np.sin(self.azimuth)*.01,
            dy*.01,
            -dxz*np.cos(self.azimuth)*.01
        )
        
    def toggle_projection(self):
        self.perspective = not self.perspective

    def get_view_matrix(self):
        return glm.lookAt(
            self.get_orbit()*self.distance + self.pan,
            self.pan,
            glm.vec3(0,1,0) if np.cos(self.elevation) < 0 else glm.vec3(0,-1,0)
        )
    
    def get_projection_matrix(self):
        return (
            glm.ortho(-self.distance, self.distance, -self.distance, self.distance, -self.distance*5, self.distance*5) if not self.perspective 
            else glm.perspective(glm.radians(45.), 1, .01, 1000)
            )
        

camera = Camera()
