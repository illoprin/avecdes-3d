from src.settings import *
from src.physics.aabb import AABB
from src.entity.entity import Entity

class PhysicsWorld():
	def __init__(self, gravity: tuple) -> None:
		self.colliders: list[Entity] = []
		self.gravity = glm.vec3(*gravity)

	def add(self, entity: Entity):
		if entity.collider_type == 'none':
			return
		else:
			obj_aabb = self.get_aabb(entity)
			self.colliders.append(obj_aabb)

	def update(self, delta_time):
		pass

	def resolve_collision(self):
		pass

	def get_aabb(self, entity):
		return AABB(self, entity)