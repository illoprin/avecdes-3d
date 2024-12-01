from src.settings import *
from dataclasses import dataclass, fields
from enum import Enum

class LightType(IntEnum):
	Empty = 0
	Ambient = 1
	Point = 2
	Spot = 3
	Sun = 4

@dataclass
class Light:
	type = LightType.Empty
	index = 0
	color: glm.vec3 # r g b represented float from 0.0 to 1.0

class AmbientLight(Light):
	type = LightType.Ambient

@dataclass
class PointLight(Light):
	type = LightType.Point
	position: glm.vec3
	intensity: float = 10.2
	radius: float = 5.0 # meters
	specular: float = 10.0

@dataclass
class SpotLight(Light):
	type = LightType.Spot
	position: glm.vec3
	direction: glm.vec3
	distance: float = 5.4 # distance of spotlight in meters
	intensity: float = 7.23
	outer_cut_off: float = glm.cos(glm.radians(34.5)) # cos range of inner cone in radians
	cutoff: float = glm.cos(glm.radians(10.2)) # cos range of outer cone in radians

@dataclass
class SunLight(Light):
	direction: glm.vec3
	intensity: float = 1.0