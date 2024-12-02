from src.settings import *

class BaseEntity():
	def __init__(self,
		name='initial_entity',
		pos=(0,0,0),
		rot=(0,0,0),
		scl=(1,1,1),
	):
		self._name = name
		# Transforms
		self.position = glm.vec3(pos)
		self.rotation = glm.vec3(rot)
		self.scale = glm.vec3(scl)
		self.update()

	@property
	def name(self):
		return f'Entity.{self._name}'

	def set_model(self, pos, rot, scl):
		model = glm.mat4x4(1.0)
		model = glm.scale(model, scl)
		pitch, yaw, roll = rot
		model = glm.rotate(model, glm.radians(pitch), (1, 0, 0))
		model = glm.rotate(model, glm.radians(yaw), (0, 1, 0))
		model = glm.rotate(model, glm.radians(roll), (0, 0, 1))
		model = glm.translate(model, pos)
		self.model = model
	
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