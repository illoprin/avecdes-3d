from src.physics.physics_engine import *
from src.entity.base_entity import BaseEntity
from src.settings import *

class AABB(Collider):
	tag = ColliderType.AABB
	def __init__(self, entity: BaseEntity, width = None, height = None, depth = None):
		self.half_scale = glm.vec3(width / 2, height / 2, depth / 2) if width != None else entity.scale / 2
		self.entity = entity
		print (f'AABB {self.entity.name}: Collider has half_scale bounds {self.half_scale.to_tuple()}')

	@property
	def position(self):
		return self.entity.position

	@property
	def min(self):
		return [
			self.position.x - self.half_scale.x,
			self.position.y - self.half_scale.y, 
			self.position.z - self.half_scale.z, 
		]
	
	@property
	def max(self):
		return [
			self.position.x + self.half_scale.x,
			self.position.y + self.half_scale.y,
			self.position.z + self.half_scale.z,
		]
	
	@staticmethod
	def get_points(pos, scl):
		return [
			# Front face SELF
			pos - glm.vec3(scl.x / 2, scl.y / 2, -scl.z / 2),
			pos + glm.vec3(scl.x / 2, -scl.y / 2, -scl.z / 2),
			pos + glm.vec3(-scl.x / 2, scl.y / 2, -scl.z / 2),
			pos + glm.vec3(scl.x / 2, scl.y / 2, -scl.z / 2),
			# Back face SELF
			pos + glm.vec3(-scl.x / 2, -scl.y / 2, scl.z / 2),
			pos + glm.vec3(scl.x / 2, -scl.y / 2, scl.z / 2),
			pos + glm.vec3(scl.x / 2, scl.y / 2, scl.z / 2),
			pos + glm.vec3(-scl.x / 2, scl.y / 2, scl.z / 2)
		]