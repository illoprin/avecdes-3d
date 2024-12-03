from src.physics.physics_engine import CollisionTag
from src.entity.base_entity import BaseEntity
from src.physics.rigidbody import Rigidbody
from src.shader_program import Shader
from src.player.camera import Camera
from src.physics.aabb import AABB
from src.settings import *

class FPSController(BaseEntity):
	def __init__ (self, app, shader: Shader, pos=(0,0,0)):
		super().__init__(name='player', pos=pos)
		# Helper entity, only contains aabb and rigidbody
		self.tag = EntityTypes.Helper

		self.app = app
		self.wnd = app.wnd
		self.movement_velocity = PLAYER_SPEED
		
		# Set player bounds
		self._scale = glm.vec3(1, 1.8, 1)

		self.collider = AABB(self)
		self.rigidbody = Rigidbody(CollisionTag.Dynamic, mass=63, use_gravity=True)
		self.camera = Camera(shader)
		self.camera_jitter = glm.vec3(0.0)

		# Init keyboard input
		self.keyboard_statements = {
			self.wnd.keys.W: False,
			self.wnd.keys.S: False,
			self.wnd.keys.A: False,
			self.wnd.keys.D: False,
		}
		self.walking = False

	def update(self):
		pass
	
	def update_player(self):
		self.camera_effects()
		self.camera.position = self._position + glm.vec3(0, PLAYER_H/2, 0) + self.camera_jitter
		self.rigidbody.velocity *= 0.5
		self.camera.update()

	def handle_keyboard(self, key, action, modifer):
		if action == self.wnd.keys.ACTION_PRESS:
			if key in self.keyboard_statements:
				self.keyboard_statements[key] = True
				self.walking = True
			if key == self.wnd.keys.SPACE:
				# self.jump()
				pass
			if modifer == self.wnd.modifiers.ctrl:
				self.movement_velocity = PLAYER_SPEED * PLAYER_SPEED_MODIFER
		if action == self.wnd.keys.ACTION_RELEASE:
			if key in self.keyboard_statements:
				self.keyboard_statements[key] = False
				self.walking = False
			self.movement_velocity = PLAYER_SPEED

	def handle_mouse(self, dx, dy):
		self.camera.rotate_yaw(dx * PLAYER_SENSITIVITY)
		self.camera.rotate_pitch(-dy * PLAYER_SENSITIVITY)
		self._rotation.y += dx

	def movement(self):
		vel = self.movement_velocity
		self.forward = glm.vec3(self.camera.forward.x, 0, self.camera.forward.z)
		self.right = glm.vec3(self.camera.right.x, 0, self.camera.right.z)
		if self.rigidbody.grounded and self.walking:
			if self.keyboard_statements.get(self.wnd.keys.W):
				self.rigidbody.add_force(self.forward * vel)
			if self.keyboard_statements.get(self.wnd.keys.S):
				self.rigidbody.add_force(-self.forward * vel)
			if self.keyboard_statements.get(self.wnd.keys.A):
				self.rigidbody.add_force(-self.right * vel)
			if self.keyboard_statements.get(self.wnd.keys.D):
				self.rigidbody.add_force(self.right * vel)
		
		elif not self.walking:
			self.rigidbody.acceleration *= .97

	def jump(self):
		if self.rigidbody.grounded:
			self.rigidbody.grounded = False
			self.rigidbody.add_force(glm.vec3(0, 1, 0) * PLAYER_SPEED * 800)
	

	def camera_effects(self):
		print(self.rigidbody.grounded)
		ratio = glm.length(self.rigidbody.acceleration)/self.movement_velocity
		y = glm.cos(self.app.time*8) * .025
		self.camera_jitter = glm.vec3(0, y, 0) * ratio

	

	

		
