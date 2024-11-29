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
		self.acceleration = glm.vec3(*start_acceleration)
		self.velocity = glm.vec3(*start_velocity)
		self.delta_time = 0

	def update(self, delta_time):
		self.delta_time = delta_time
		self.velocity += self.acceleration
		if self.use_gravity:
			self.velocity += PHYS_GRAVITY
		self.velocity *= PHYS_WINDAGE * self.delta_time

	def add_force (self, force=(0, 0, 0)):
		self.acceleration = glm.vec3(*force) * self.mass

	def zero_velocity (self):
		self.velocity = glm.vec3(0)
		self.acceleration = glm.vec3(0)