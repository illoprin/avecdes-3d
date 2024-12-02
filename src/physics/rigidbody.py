from src.settings import *
from src.physics.physics_engine import CollisionTag, gravity_collinear

# TODO: Решить проблему с телами, которые лежат друг на друге
#	Сейчас их grounded = False даже когда они уже лежат друг на друге

class Rigidbody():
	def __init__(self,
		tag: CollisionTag,
		mass = 1.0,
		use_gravity = False,
		start_velocity = (0, 0, 0),
		start_acceleration = (0, 0, 0)
	):
		self.tag = tag
		self.mass = mass
		self.use_gravity = use_gravity
		self.acceleration = glm.vec3(start_acceleration)
		self.velocity = glm.vec3(start_velocity)
		self.delta_time = 0
		self.shift = glm.vec3()
		self.grounded = False

	def update(self, delta_time):
		self.delta_time = delta_time
		self.velocity += self.acceleration
		# If using gravity
		if self.use_gravity and not self.grounded:
			self.velocity += PHYS_GRAVITY
		elif self.grounded:
			self.reset_velocity()
		##################
		# print (self.grounded)
		self.velocity *= PHYS_WINDAGE * self.delta_time

	def add_force (self, vec: glm.vec3):
		if self.grounded and not gravity_collinear(vec): self.grounded = False
		self.acceleration = vec / self.mass

	def reset_velocity (self):
		self.velocity = glm.vec3(0)

	def reset_acceleration (self):
		self.acceleration = glm.vec3(0)