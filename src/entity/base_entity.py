from src.settings import *
from copy import deepcopy

def exceed_theshold(a: glm.vec3, b: glm.vec3):
	# print (a, b)
	return glm.length(glm.abs(a - b)) > UPDATE_TRESHOLD 

class BaseEntity():
	def __init__(self,
		name='initial_entity',
		pos=(0,0,0),
		rot=(0,0,0),
		scl=(1,1,1),
		origin=(0,0,0)
	):
		self._name = name
		self.tag = EntityTypes.Main

		# Transforms
		self._position = glm.vec3(pos)
		self._rotation = glm.vec3(rot)
		self._scale = glm.vec3(scl)

		# Init last transforms
		# Needed for optimizing buffer update calls
		# DEEPCOPY need to create separate object in memory
		self.last_position = deepcopy(self._position)
		self.last_rotation = deepcopy(self._rotation)
		self.last_scale = deepcopy(self._scale)
		self._alive = True

		self._origin = glm.vec3(origin)
		if self.tag == EntityTypes.Main: self.update()
		self.need_redraw = True

	@property
	def name(self):
		return f'Entity.{self._name}'
	
	def get_alive(self):
		return self._alive
	def set_alive(self, value):
		self._alive = value
		self.need_redraw = True
		
	alive = property(get_alive, set_alive)
	
	def set_position(self, value: glm.vec3):
		if exceed_theshold(self._position, self.last_position) and self._alive:
			# print (f'{self.name}: Position changed. Needs buffer update')
			self._position = value
			self.last_position = deepcopy(self.position)
			self.need_redraw = True
	def set_rotation(self, value: glm.vec3):
		# print (f'{self.name}: Rotation changed. Needs buffer update')
		if exceed_theshold(self._rotation, self.last_rotation) and self._alive:
			# print (f'{self.name}: Position changed. Needs buffer update')
			self._rotation = value
			self.last_rotation = deepcopy(self.rotation)
			self.need_redraw = True
	def set_scale(self, value: glm.vec3):
		# print (f'{self.name}: Scale changed. Needs buffer update')
		if exceed_theshold(self._scale, self.last_scale) and self._alive:
			self._scale = value
			self.last_scale = deepcopy(self.last_scale)
			self.need_redraw = True

	def get_position(self):
		return self._position
	
	def get_rotation(self):
		return self._rotation
	
	def get_scale(self):
		return self._scale
	
	position = property(get_position, set_position)
	rotation = property(get_rotation, set_rotation)
	scale = property(get_scale, set_scale)
	
	def set_model(self, pos, rot, scl):
		model = glm.mat4x4(1.0)
		model = glm.scale(model, scl)
		pitch, yaw, roll = rot
		model = glm.rotate(model, glm.radians(pitch), (1, 0, 0))
		model = glm.rotate(model, glm.radians(yaw), (0, 1, 0))
		model = glm.rotate(model, glm.radians(roll), (0, 0, 1))
		model = glm.translate(model, pos)
		self.model = model * glm.translate(glm.mat4x4(1.0), self._origin)
	
	def rotate(self, rotation=(0, 0, 0)):
		pitch, yaw, roll = rotation
		self.model = glm.rotate(self.model, glm.radians(pitch), (1, 0, 0))
		self.model = glm.rotate(self.model, glm.radians(yaw), (0, 1, 0))
		self.model = glm.rotate(self.model, glm.radians(roll), (0, 0, 1))
		self.rotation += glm.vec3(rotation)

	def resize(self, scale=(1, 1, 1)):
		self.model = glm.scale(self.model, glm.vec3(scale))
		self.scale *= glm.vec3(scale)

	def update(self):
		if self.alive:
			self.set_model(self.position, self.rotation, self.scale)
		else:
			self.model = glm.mat4x4(0.0)

	def render(self) -> None: pass

	def clear(self) -> None:
		print (f'{self.name}: Cleared')