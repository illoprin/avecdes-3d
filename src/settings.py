from enum import IntEnum
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

class TextureSlot(IntEnum):
	SceneColorBuffer = 0
	SceneDepthBuffer = 1
	DiffuseMap = 2
	NormalMap = 3
	LevelTextureArray = 4
	ClusterDiffuseMap = 5

# World dirs
DIR_UP = glm.vec3(0, 1, 0)
DIR_FORWARD = glm.vec3(0, 0, 1)
DIR_RIGHT = glm.vec3(1, 0, 0)

# Resources control
MAX_NOT_INSTANCED_OBJECTS_PER_SCENE: int = 128
MAX_OBJECTS_PER_CLUSTER: int = 2048
FLOAT32_BYTE_SIZE: int = 64
UPDATE_TRESHOLD: float = 0.02

# Camera
CAM_FOV = math.pi / 2 + math.pi / 4
CAM_FOV_V = CAM_FOV
CAM_FOV_H = 2 * glm.tan(glm.atan(CAM_FOV_V / 2) * WIN_ASPECT)
CAM_NEAR_FAR = (0.01, 500.0)
CAM_MAX_PITCH = math.pi / 2

# Player
PLAYER_SPEED = 3.5
PLAYER_SENSITIVITY = 0.1
PLAYER_SPEED_MODIFER = 4.0
PLAYER_H = 2

# Physics
PHYS_GRAVITY = glm.vec3(0, -9.81, 0)
PHYS_WINDAGE = 0.76 # Air resistance
PHYS_MIN_Y = -10
