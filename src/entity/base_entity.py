from src.settings import *

class BaseEntity():
	def __init__(self,
		name='initial_entity',
		pos=(0,0,0),
		rot=(0,0,0),
		scl=(1,1,1),
		origin=(0,0,0)
	):
		self._name = name
		# Transforms
		self._position = glm.vec3(pos)
		self._rotation = glm.vec3(rot)
		self._scale = glm.vec3(scl)
		self._origin = glm.vec3(origin)
		self.update()
		self.need_redraw = True

	@property
	def name(self):
		return f'Entity.{self._name}'
	
	def set_position(self, value: glm.vec3):
		# print (f'{self.name}: Position changed. Needs buffer update')
		self._position = value
		self.need_redraw = True
	def set_rotation(self, value: glm.vec3):
		# print (f'{self.name}: Rotation changed. Needs buffer update')
		self._rotation = value
		self.need_redraw = True
	def set_scale(self, value: glm.vec3):
		# print (f'{self.name}: Scale changed. Needs buffer update')
		self._scale = value
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
		self.set_model(self.position, self.rotation, self.scale)

	def render(self) -> None: pass

	def clear(self) -> None:
		print (f'{self.name}: Cleared')