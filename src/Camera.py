'''
Author: William Abrahamsson
Mail: william_abrahamsson@outlook.com
    (alt): wa222dt@student.lnu.se

Digital Museum
'''

import numpy as np
from OpenGL.GL import *
import sdl2
import sdl2.video

class Camera:
    
    '''
    Represents a camera in a 3D scene, capable of projection and view transformations.
    '''

    def __init__(self, shader):

        '''
        Initializes the camera with a specific shader and sets up the initial projection matrix.

        Args:
            shader (int): The shader program ID to be used for rendering.
        '''
        
        self.rotation_angle_degrees = 0.0
        self.shader = shader
        
        self.projection_transform = self.get_projection_mx(90, 800/600, 0.1, 10)
        

    def start(self):

        '''
        Initializes or resets the camera's rotation angle to zero and updates the projection.
        '''
        
        self.rotation_angle_degrees == 0.0
        self.tell_shader()
    
    def rotate(self, dir):

        '''
        Updates the camera's rotation angle based on the input direction.

        Args:
            dir: The direction to rotate the camera. Accepts "left" or "right".
        '''
        
        if (dir == "right"):
            self.rotation_angle_degrees -= 5.0
        elif (dir == "left"):
            self.rotation_angle_degrees += 5.0
        
        self.tell_shader()
        
    def get_projection_mx(self, fov, aspect_ratio, near, far) -> np.ndarray:
        
        '''
        Computes the perspective projection matrix.

        Args:
            fov (float): Field of view angle in degrees.
            aspect_ratio (float): Aspect ratio of the viewport (width / height).
            near (float): Distance to the near clipping plane.
            far (float): Distance to the far clipping plane.

        Returns:
            numpy.ndarray: The computed perspective projection matrix.
        '''

        f = 1.0 / np.tan(np.radians(fov) / 2)
        nf = 1 / (near - far)

        return np.array([
            [f / aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) * nf, -1],
            [0, 0, 2 * far * near * nf, 0]
        ], dtype=np.float32)

    
    def get_rotation_mx(self) -> np.ndarray:
        
        '''
        Computes the rotation matrix depending on rotation from user input
        in rotation function.
        
        Returns:
        numpy.ndarray: The computed rotation matrix.
        '''
        
        # rotation matrix on y-axis.
        radian_angle = np.radians(self.rotation_angle_degrees)
        
        return np.array([
            [np.cos(radian_angle), 0, np.sin(radian_angle), 0],
            [0, 1, 0, 0],
            [-np.sin(radian_angle), 0, np.cos(radian_angle), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
    def tell_shader(self):
        
        '''
        Applies the current rotation to the projection transform and updates the shader's
        projection matrix uniform.
        '''
        
        # set the uniform matrix in shader.
        glUniformMatrix4fv(
            glGetUniformLocation(
                self.shader,
                "projection"
            ),
            1,
            GL_FALSE,
            np.dot(
                self.get_rotation_mx(),
                self.projection_transform
            )
        )
              


