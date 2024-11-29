from src.settings import *
from src.physics.aabb import AABB
from src.physics.physics_engine import *

class PhysicsWorld():
	def __init__(self, gravity: tuple) -> None:
		self.objects = []
		self.collision_pairs = []
		self.gravity = glm.vec3(*gravity)

	def add(self, entity):
		if entity.collider.tag != ColliderType.NoCollider:
			self.objects.append(entity)

	def update(self, delta_time):
		for obj in self.objects:
			self.update_rigidbodies(obj, delta_time)
			self.detect_collisions(obj)
			self.collision_responce()

	def update_rigidbodies(self, active, delta_time):
		if active.rigidbody != None:
			active.rigidbody.update(delta_time)
			active.position += active.rigidbody.velocity
		
	def detect_collisions(self, active):
		for target in self.objects:
			if active == target: continue
			active_type, target_type = active.collider.tag, target.collider.tag
			if active_type == ColliderType.AABB and target_type == ColliderType.AABB:
				collision = has_intersection_aabb_aabb(active, target) 
				if collision:
					self.collision_pairs.append([active, target])
					collision_responce = collision.responce
					active.position += collision_responce['active']
					target.position += collision_responce['target']
					if active.rigidbody != None:
						active.rigidbody.reset_velocity()
						active.rigidbody.grounded = collision_responce['active'].y > 0.0
					# print (f'PhysicsWorld: has collision of {active.name} and {target.name}\tOverlap is: {collision.overlap.to_tuple()}')

	def collision_responce(self):
		# TODO: Apply momentum responce when two rigidbodies colliding
		pass
		self.collisions = []