import glm
import numpy as np

class Camera:
    def __init__(self):
        self.distance  = 10.
        self.azimuth   = glm.degrees(30.)
        self.elevation = glm.degrees(45.)
        self.pan = glm.vec3(0.,0.,0.)  
        self.orthogonal = False
    
    # get camera position except for pos that panned  
    def get_orbit(self):
        return glm.vec3(
            np.cos(self.azimuth)*np.cos(self.elevation),
            np.sin(self.elevation),
            np.sin(self.azimuth)*np.cos(self.elevation)
        )
    
    # zoom in and out
    def increase_distance(self):
        self.distance = min(100, self.distance*1.1)
    def decrase_distance(self):
        self.distance = max(.01, self.distance*.9)
    
    # orbit
    def change_azimuth(self, diff):
        self.azimuth += diff*glm.degrees(.0001)
    def change_elevation(self, diff):
        self.elevation += diff*glm.degrees(.00007)
        
    # pan
    def change_pan(self, dx, dy):
        # get u and v vector of camera
        M = glm.transpose(self.get_view_matrix())
        u = M[0].xyz
        v = M[1].xyz
        
        # pan camera
        self.pan += -(u*dx+v*dy)*.0007*self.distance

    # when press 'v' key
    def toggle_projection(self):
        self.orthogonal = not self.orthogonal
        
    # getInstance
    def isOrthogonal(self):
        return self.orthogonal

    # get V matrix of MVP
    def get_view_matrix(self):
        return glm.lookAt(
            self.get_orbit()*self.distance + self.pan,
            self.pan,
            glm.vec3(0,1,0) if np.cos(self.elevation) < 0 else glm.vec3(0,-1,0)
        )
    
    # get P matrix of MVP
    def get_projection_matrix(self):
        return (
            glm.ortho(-self.distance*.45, self.distance*.45, -self.distance*.45, self.distance*.45, -self.distance*5, self.distance*5) if self.orthogonal
            else glm.perspective(glm.radians(45.), 1, .01, 1000)
            )

# make global camera
camera = Camera()
