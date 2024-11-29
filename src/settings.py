import moderngl as mgl
import numpy as np
import math
import glm

# OpenGL context
OPENGL_STATEMENTS = mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND

# Window
WIN_MODE = (1280, 720)
WIN_ASPECT = WIN_MODE[0] / WIN_MODE[1]
WIN_TITLE = 'Game'
WIN_CLEAR = (0.1, 0.1, 0.1)

# Resources
LEVELS_DIR = 'levels'
ASSETS_DIR = 'assets'
SHADER_DIR = 'src/shaders'
SCREENSHOTS_DIR = 'screenshots'
CACHE_DIR = 'cache'

# Texture biffer indices
SCENE_FRAMEBUFFER = 0
SCENE_DEPTH_FRAMEBUFFER = 1
DEFAULT_TEXTURE = 2
LEVEL_TEXARRAY = 3

# World dirs
DIR_UP = glm.vec3(0, 1, 0)
DIR_FORWARD = glm.vec3(0, 0, 1)
DIR_RIGHT = glm.vec3(1, 0, 0)

# Camera
CAM_FOV = 90
CAM_FOV_V = glm.radians(CAM_FOV)
CAM_FOV_H = 2 * glm.tan(glm.atan(CAM_FOV_V / 2) * WIN_ASPECT)
CAM_NEAR_FAR = (0.01, 5000.0)
CAM_MAX_PITCH = math.pi / 2

# Player
PLAYER_SPEED = 2
PLAYER_SENSITIVITY = 0.1
PLAYER_SPEED_MODIFER = 2.0
PLAYER_H = 2

# Physics
PHYS_GRAVITY = glm.vec3(0, -9.81, 0)
PHYS_WINDAGE = 0.76 # Air resistance
