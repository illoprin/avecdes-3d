from src.settings import *
from src.physics.aabb import AABB
from src.physics.physics_engine import *

class PhysicsWorld():
	def __init__(self, gravity: tuple) -> None:
		self.objects: list[Entity] = []
		self.collisions: list[Collision] = []
		self.gravity = glm.vec3(*gravity)
		self.delta_time = 1

	def add(self, entity: Entity):
		self.colliders.append(entity)

	def update(self, delta_time):
		self.delta_time = delta_time
		self.update_rigidbodies()
		self.detect_collisions()
		self.resolve_collisions()

	def update_rigidbodies(self):
		for obj in self.objects:
			if obj.rigidbody:
				obj.rigidbody.update(self.delta_time)
	
	def detect_collisions(self):
		for a_obj in self.objects:
			for b_obj in self.objects:
				if a_obj == b_obj: continue
				if has_intersection_aabb_aabb(a_obj, b_obj):
					self.collisions.append(Collision(a_obj, b_obj))

	def resolve_collisions(self):
		for collision in self.collisions:
			if collision.obj_a.collider.tag == ColliderType.AABB and collision.obj_b.collider.tag == ColliderType.AABB:
				resolve_collision_aabb_aabb(collision.obj_a, collision.obj_b)  
	
	def resolve_collision(self, a_obj, b_obj):
		print (f'Has collision with {a_obj.name} and {b_obj.name}')