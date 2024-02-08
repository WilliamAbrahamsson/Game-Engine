'''
Author: William Abrahamsson
Mail: william_abrahamsson@outlook.com
    (alt): wa222dt@student.lnu.se

Digital Museum
'''

from Scene import Scene
from Cube import Cube
from OpenGL.GL import *

scene = Scene()

# room is a cube (camera is inside)
room = Cube(
    position=[0, 0, 0],
    angles=[0, 0, 0],
    scale=[10, 10, 10],
    angular_velocity=[0, 0, 0],
    texture_path="textures/walls/white.png"
)
scene.add_object(room)

floor = Cube(
    position=[0, -5, 0],
    angles=[90, 0, 90],
    scale=[10, 10, 1],
    angular_velocity=[0, 0, 0],
    texture_path="textures/walls/bricks.jpg"
)
scene.add_object(floor)

roof = Cube(
    position=[0, 5, 0],
    angles=[-90, 0, 0],
    scale=[10, 10, 1],
    angular_velocity=[0, 0, 0],
    texture_path="textures/walls/putty.png"
)
scene.add_object(roof)


front_frame = Cube(
    position=[0, 0, -5],
    angles=[0, 0, 0],
    scale=[7, 6, 1],
    angular_velocity=[0, 0, 0],
    texture_path="textures/frames/silver.png"
)
scene.add_object(front_frame)

front_painting = Cube(
    position=[0, 0, -4],
    angles=[0, 0, 180],
    scale=[6.1, 5.2, 0],
    angular_velocity=[0, 0, 0],
    texture_path="textures/paintings/vangough.png"
)
scene.add_object(front_painting)

left_frame = Cube(
    position=[-5, 0, 0],
    angles=[0, 90, 0],
    scale=[7, 7, 1],
    angular_velocity=[0, 0, 0],
    texture_path="textures/frames/gold.png"
)
scene.add_object(left_frame)

left_painting = Cube(
    position=[-4, 0, 0],
    angles=[0, 90, 180],
    scale=[6, 6, 0],
    angular_velocity=[0, 0, 0],
    texture_path="textures/paintings/monalisa.png"
)
scene.add_object(left_painting)

right_frame = Cube(
    position=[5, 0, 0],
    angles=[0, -90, 0],
    scale=[7, 3.6, 1],
    angular_velocity=[0, 0, 0],
    texture_path="textures/frames/wood.png"
)
scene.add_object(right_frame)

right_painting = Cube(
    position=[4, 0, 0],
    angles=[0, -90, 180],
    scale=[6, 3, 0],
    angular_velocity=[0, 0, 0],
    texture_path="textures/paintings/lastsupper.jpeg"
)
scene.add_object(right_painting)

back_frame = Cube(
    position=[0, 0, 5],
    angles=[0, 180, 0],
    scale=[7, 4.7, 1],
    angular_velocity=[0, 0, 0],
    texture_path="textures/frames/stone.png"
)
scene.add_object(back_frame)

back_painting = Cube(
    position=[0, 0, 4],
    angles=[0, 180, 180],
    scale=[6, 4, 0],
    angular_velocity=[0, 0, 0],
    texture_path="textures/paintings/abstract.jpeg"
)
scene.add_object(back_painting)

scene.run()
