from src.settings import *
from src.entity.entity import Entity
from src.physics.physics_world import PhysicsWorld

class AABB():
	def __init__(self, physics_world: PhysicsWorld, entity: Entity):
		self.entity = entity
		self.physics_world = physics_world
		
	def detect_collision(self, other_aabb):
		scl_a = self.entity.scale
		pos_a = self.entity.position
		points_a = self.get_points(pos_a, scl_a)

		scl_b = other_aabb.entity.scale
		pos_b = other_aabb.entity.position
		points_b = self.get_points(pos_b, scl_b)

		return self.has_intersection(points_a, points_b)

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
	
	def has_intersection(self, points_a, points_b):
		return False