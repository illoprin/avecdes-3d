from src.settings import *

class Rigidbody():
	def __init__(self,
		mass = 1.0, 
		use_gravity = False,
		start_velocity = (0, 0, 0),
		start_acceleration = (0, 0, 0)
	):
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
		##################
		self.velocity *= PHYS_WINDAGE * self.delta_time

	def add_force (self, vec: glm.vec3):
		self.acceleration = vec / self.mass

	def reset_velocity (self):
		self.velocity = glm.vec3(0)

	def reset_acceleration (self):
		self.acceleration = glm.vec3(0)