'''
Author: William Abrahamsson
Mail: william_abrahamsson@outlook.com
    (alt): wa222dt@student.lnu.se

Digital Museum
'''

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from sdl2 import *
from sdl2.video import *
from Camera import Camera
import numpy as np

class Scene:

    def __init__(self):
        
        '''
        Initializes the scene, setting up the SDL window, OpenGL context,
        shaders, and camera.
        '''

        self.objects = []
        self.rotation_angle_degrees = 0.0

        # setup.
        SDL_Init(SDL_INIT_VIDEO)
        
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3)
        
        SDL_GL_SetAttribute(
            SDL_GL_CONTEXT_PROFILE_MASK,
            SDL_GL_CONTEXT_PROFILE_CORE
        )
        
        window_title = b"OpenGL - Assignment 3"
        self.window = SDL_CreateWindow(
            window_title,
            SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
            800,
            600,
            SDL_WINDOW_OPENGL
        )
        
        self.gl_context = SDL_GL_CreateContext(self.window)

        # timer.
        self.clock = SDL_GetTicks()

        # set background.
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # load shaders.
        self.shader = self.create_shader(
            vertex_filepath="shaders/vertex.glsl",
            fragment_filepath="shaders/fragment.glsl"
        )

        # use the shaders.
        glUseProgram(self.shader)

        self.set_shader_variables()
        
        self.camera = Camera(self.shader)

        glUniform1i(self.texUniform, 0)
        glUniform3f(self.lightPosLocation, 0.0, 5.0, 0.0)
        
    def set_shader_variables(self):
        
        '''
        Set the shader variables that are used when sending data to
        the shaders.
        '''
        
        # shader variables
        self.texUniform = glGetUniformLocation(self.shader, "imageTexture")
        self.viewMatrixLocation = glGetUniformLocation(self.shader, "view")
        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")
        self.lightPosLocation = glGetUniformLocation(self.shader, "lightPos")
    
    def create_shader(self, vertex_filepath: str, fragment_filepath: str) -> int:

        '''
        Compiles vertex and fragment shaders from file paths, linking them into a
        shader program.

        Args:
            vertex_filepath: The file path to the vertex shader source code.
            fragment_filepath: The file path to the fragment shader source code.

        Returns:
            The compiled shader program ID.
        '''
        
        with open(vertex_filepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragment_filepath, 'r') as f:
            fragment_src = f.readlines()

        return compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER), 
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )
    
    def add_object(self, obj):
        
        '''
        Adds an object (Cube) to the scene's render list.

        Args:
            obj: The object to be added, expected to have a display method.
        '''
        
        self.objects.append(obj)

    def display(self):
        
        '''
        Clears the screen and renders all objects in the scene, updating
        the view and model matrices.
        '''
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for index, obj in enumerate(self.objects):
            # activate correct texture according to index (GL_TEXTURE0, GL_TEXTURE1 ...)
            obj.display(self.shader)

    def run(self):
        
        '''
        Enters the main event loop, handling keyboard input and updating
        the scene continuously.
        '''
        
        running = True
        event = SDL_Event()
        while running:

            # keyboard interaction (a: left, d: right)
            while SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_KEYDOWN:
                    if event.key.keysym.sym == SDLK_a:
                        self.camera.rotate("left")
                    if event.key.keysym.sym == SDLK_d:
                        self.camera.rotate("right")
                        
            # update cubes.
            self.display()

            self.camera.start()

            SDL_GL_SwapWindow(self.window)
