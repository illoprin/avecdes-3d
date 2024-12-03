from src.settings import *
from src.physics.aabb import AABB
from src.entity.entity import Entity
from src.entity.base_entity import BaseEntity
from src.physics.physics_engine import *

class PhysicsWorld():
	def __init__(self, gravity: tuple) -> None:
		self.objects: list[BaseEntity] = []
		self.collision_pairs = []
		self.gravity = glm.vec3(*gravity)

	def add(self, entity):
		if entity.collider.tag != ColliderType.NoCollider:
			self.objects.append(entity)

	def update(self, delta_time):
		for obj in self.objects:
			if obj.alive:
				self.update_rigidbodies(obj, delta_time)
				self.detect_collisions(obj)
				self.collision_responce()
				self.clear_extra(obj)
		
	def update_rigidbodies(self, active: BaseEntity, delta_time):
		if active.rigidbody.tag == CollisionTag.Dynamic:
			active.rigidbody.update(delta_time)
			active.position += active.rigidbody.velocity
		
	def detect_collisions(self, active: BaseEntity):
		for target in self.objects:
			if active == target: continue
			active_type, target_type = active.collider.tag, target.collider.tag
			if active_type == ColliderType.AABB and target_type == ColliderType.AABB:
				collision = has_intersection_aabb_aabb(active, target)
				if collision:
					self.collision_pairs.append([active, target, collision])

	def collision_responce(self):
		for active, target, collision in self.collision_pairs:
			collision_responce = collision.responce
			active.position += collision_responce['active']
			target.position += collision_responce['target']
			if not glm.length(collision_responce['active']) == 0:
				active.rigidbody.grounded = gravity_collinear(collision_responce['active'])
			if not glm.length(collision_responce['target']) == 0:
				target.rigidbody.grounded = gravity_collinear(-collision_responce['target'])
			active.rigidbody.last_collision = collision_responce['active']
			target.rigidbody.last_collision = collision_responce['target']
			# TODO: Apply momentum responce when two rigidbodies colliding
		self.collision_pairs = []

	def clear_extra(self, active: BaseEntity):
		if active.position.y < PHYS_MIN_Y:
			if active.tag == EntityTypes.Main:
				active.alive = False
			if active.tag == EntityTypes.Helper:
				active.position = glm.vec3(0, 3, 0)
				print (active.name)