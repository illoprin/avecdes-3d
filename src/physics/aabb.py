from src.settings import *
from src.physics.physics_engine import *

class AABB(Collider):
	tag = ColliderType.AABB
	def __init__(self, entity: Entity):
		self.entity = entity
	
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