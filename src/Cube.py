'''
Author: William Abrahamsson
Mail: william_abrahamsson@outlook.com
    (alt): wa222dt@student.lnu.se

Digital Museum
'''

from OpenGL.GL import *
import numpy as np
from PIL import Image

class Cube:
    
    '''
    Represents a 3D object within a scene, including its geometry, texture, and transformations.
    '''

    def __init__(self, position: list[float], angles: list[float], scale: list[float], angular_velocity: list[float], texture_path: str):
        
        '''
        Initializes a new 3D object with specified position, orientation, scale, angular velocity, and texture.

        Args:
            position: Initial position of the object in 3D space.
            angles: Initial orientation of the object represented by Euler angles.
            scale: Scale factors along the X, Y, and Z axes.
            angular_velocity: Angular velocity for each of the Euler angles.
            texture_path: Path to the texture image file.
        '''

        # initialize params into object.
        self.position = np.array(position, dtype=np.float32)
        self.angles = np.array(angles, dtype=np.float32)
        self.angular_velocity = np.array(angular_velocity, dtype=np.float32)
        self.scale = np.array(scale, dtype=np.float32)
        self.texture_path = texture_path

        # 3D Space: (x, y, z), Texture: (u, v)
        self.vertices = (
            # front face
            -0.5, -0.5, -0.5, 0, 0,
            0.5, -0.5, -0.5, 1, 0,
            0.5,  0.5, -0.5, 1, 1,
            0.5,  0.5, -0.5, 1, 1,
            -0.5,  0.5, -0.5, 0, 1,
            -0.5, -0.5, -0.5, 0, 0,

            # back face
            -0.5, -0.5,  0.5, 1, 0,
            0.5, -0.5,  0.5, 0, 0,
            0.5,  0.5,  0.5, 0, 1,
            0.5,  0.5,  0.5, 0, 1,
            -0.5,  0.5,  0.5, 1, 1,
            -0.5, -0.5,  0.5, 1, 0,

            # left face
            -0.5, -0.5, -0.5, 0, 0,
            -0.5, -0.5,  0.5, 1, 0,
            -0.5,  0.5,  0.5, 1, 1,
            -0.5,  0.5,  0.5, 1, 1,
            -0.5,  0.5, -0.5, 0, 1,
            -0.5, -0.5, -0.5, 0, 0,

            # right face
            0.5, -0.5, -0.5, 1, 0,
            0.5, -0.5,  0.5, 0, 0,
            0.5,  0.5,  0.5, 0, 1,
            0.5,  0.5,  0.5, 0, 1,
            0.5,  0.5, -0.5, 1, 1,
            0.5, -0.5, -0.5, 1, 0,

            # top face
            -0.5, -0.5,  0.5, 0, 1,
            0.5, -0.5,  0.5, 1, 1,
            0.5, -0.5, -0.5, 1, 0,
            0.5, -0.5, -0.5, 1, 0,
            -0.5, -0.5, -0.5, 0, 0,
            -0.5, -0.5,  0.5, 0, 1,

            # bottom face
            -0.5,  0.5,  0.5, 0, 0,
            0.5,  0.5,  0.5, 1, 0,
            0.5,  0.5, -0.5, 1, 1,
            0.5,  0.5, -0.5, 1, 1,
            -0.5,  0.5, -0.5, 0, 1,
            -0.5,  0.5,  0.5, 0, 0
        )

        self.vertex_count = len(self.vertices) // 5
        self.vertices = np.array(self.vertices, dtype=np.float32)

        # Create VAO and VBOs
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo_vertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_vertices)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes,
                     self.vertices, GL_STATIC_DRAW)

        # Vertex positions
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))

        # Texture coordinates
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                              20, ctypes.c_void_p(12))

        self.create_texture()

        # Normals for each face of the cube (nx, ny, nz).
        self.normals = (
            # front face
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,

            # back face
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,

            # left face
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,

            # right face
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,

            # top face
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,

            # bottom face
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0
        )

        # Create a VBO for normals
        self.normals = np.array(self.normals, dtype=np.float32)
        self.vbo_normals = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_normals)
        glBufferData(GL_ARRAY_BUFFER, self.normals.nbytes,
                     self.normals, GL_STATIC_DRAW)

        # Normals attribute
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

    def get_identity_mx(self) -> np.ndarray:
        
        '''
        Generates an identity matrix.

        Returns:
            A 4x4 identity matrix as a numpy array of type float32.
        '''
        
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype = np.float32)
        
    def get_scale_mx(self) -> np.ndarray:
        
        '''
        Creates a scaling matrix based on the object's scale attributes.

        Returns:
            A 4x4 scaling matrix as a numpy array of type float32.
        '''
        
        scale_x = self.scale[0]
        scale_y = self.scale[1]
        scale_z = self.scale[2]
        
        return np.array([
            [scale_x, 0, 0, 0],
            [0, scale_y, 0, 0],
            [0, 0, scale_z, 0],
            [0, 0, 0, 1]
        ], dtype = np.float32)

    def get_rotation_mx(self) -> np.ndarray:
        
        '''
        Constructs a rotation matrix from the object's Euler angles.

        Returns:
            A 4x4 rotation matrix as a numpy array of type float32, representing
            the combined rotation around the x, y, and z axes.
        '''
        
        angle_x = np.radians(self.angles[0])
        angle_y = np.radians(self.angles[1])
        angle_z = np.radians(self.angles[2])
        
        rotation_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(angle_x), -np.sin(angle_x), 0],
            [0, np.sin(angle_x), np.cos(angle_x), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        rotation_y = np.array([
            [np.cos(angle_y), 0, np.sin(angle_y), 0],
            [0, 1, 0, 0],
            [-np.sin(angle_y), 0, np.cos(angle_y), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        rotation_z = np.array([
            [np.cos(angle_z), -np.sin(angle_z), 0, 0],
            [np.sin(angle_z), np.cos(angle_z), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        rotation_matrix = np.dot(rotation_z, rotation_y)
        return np.dot(rotation_matrix, rotation_x)
        
            
    def get_translation_mx(self) -> np.ndarray:
        
        '''
        Produces a translation matrix based on the object's position.

        Returns:
            A 4x4 translation matrix as a numpy array of type float32.
        '''
        
        pos_x = self.position[0]
        pos_y = self.position[1]
        pos_z = self.position[2]
        
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [pos_x, pos_y, pos_z, 1]
        ], dtype=np.float32)
                
    def transform(self) -> np.ndarray:

        '''
        Computes the object's model transformation matrix by applying scale, rotation, and translation.

        Returns:
            The resulting 4x4 model transformation matrix as a numpy array.
        '''

        model_transform = self.get_identity_mx()
        model_transform = np.dot(model_transform, self.get_scale_mx())
        model_transform = np.dot(model_transform, self.get_rotation_mx())
        model_transform = np.dot(model_transform, self.get_translation_mx())

        return model_transform

    def create_texture(self):
        
        '''
        Creates a texture from an image file and sets up texture parameters.
        '''
        
        # Generate a texture ID
        texture = glGenTextures(1)

        # Bind the texture
        glBindTexture(GL_TEXTURE_2D, texture)

        # Load image using PIL
        image = Image.open(self.texture_path)
        img_data = image.convert("RGBA").tobytes()  # Convert to bytes

        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # Set the texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width,
                     image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        self.texture = texture

    def use_texture(self):
        '''
        Activate and bind texture.
        '''
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        
    def tell_shader(self, shader):
        # call transform function.
        glUniformMatrix4fv(
            glGetUniformLocation(
                shader,
                "model"
            ),
            1,
            GL_FALSE,
            self.transform()
        )

    def display(self, shader):
        
        '''
        Renders the object using the current vertex array, texture, and updates its rotation.

        This method binds the object's vertex array and texture, then draws the object using
        the current vertex count. It also updates the object's angles based on its angular
        velocity, facilitating continuous rotation.
        '''

        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

        self.use_texture()

        # update angles according to angular velocity for each axis.
        self.angles[0] += self.angular_velocity[0]
        self.angles[1] += self.angular_velocity[1]
        self.angles[2] += self.angular_velocity[2]

        self.tell_shader(shader)