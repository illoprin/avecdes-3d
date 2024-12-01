from src.shader_program import Shader
from src.player.camera import Camera
from src.settings import *
import moderngl_window as mglw

class Player():
	def __init__(self, wnd: mglw.BaseWindow, shader: Shader, pos=(0, 0, 0), rot=(0, 90)):
		self.wnd = wnd
		self.camera = Camera(shader, pos, rot)
		self.position = self.camera.position

		self.keyboard_statements = {
			self.wnd.keys.W: False,
			self.wnd.keys.S: False,
			self.wnd.keys.A: False,
			self.wnd.keys.D: False,
			self.wnd.keys.Q: False,
			self.wnd.keys.E: False,
		}

		self.velocity = glm.vec3(0.0)
		self.acceleration = glm.vec3(0.0)
		self.movement_velocity = PLAYER_SPEED
		self.delta_time = 0

	def handle_keyboard(self, key, action, modifer):
		if action == self.wnd.keys.ACTION_PRESS:
			if key in self.keyboard_statements:
				self.keyboard_statements[key] = True
			
			if modifer == self.wnd.modifiers.ctrl:
				self.movement_velocity = PLAYER_SPEED * PLAYER_SPEED_MODIFER
		elif action == self.wnd.keys.ACTION_RELEASE:
			if key in self.keyboard_statements:
				self.keyboard_statements[key] = False
				self.acceleration = glm.vec3(0.0)
			self.movement_velocity = PLAYER_SPEED
	

	def handle_mouse(self, dx, dy):
		self.camera.rotate_yaw(dx * PLAYER_SENSITIVITY)
		self.camera.rotate_pitch(-dy * PLAYER_SENSITIVITY)

	def movement(self, delta_time):
		self.delta_time = delta_time
		vel = self.movement_velocity * 0.005

		if self.keyboard_statements.get(self.wnd.keys.W):
			self.acceleration += self.camera.forward
		if self.keyboard_statements.get(self.wnd.keys.S):
			self.acceleration += -self.camera.forward
		if self.keyboard_statements.get(self.wnd.keys.A):
			self.acceleration += -self.camera.right
		if self.keyboard_statements.get(self.wnd.keys.D):
			self.acceleration += self.camera.right
		if self.keyboard_statements.get(self.wnd.keys.Q):
			self.camera.move_up(PLAYER_SPEED * delta_time)
		if self.keyboard_statements.get(self.wnd.keys.E):
			self.camera.move_down(PLAYER_SPEED * delta_time)

		self.acceleration = glm.normalize(self.acceleration) if glm.length(self.acceleration) > 0 else self.acceleration
		
		self.velocity += self.acceleration * vel * self.delta_time
		if glm.length(self.velocity) > vel:
			self.velocity = glm.normalize(self.velocity) * vel
		if glm.length(self.acceleration) < .5:
			self.velocity *= 0.985

	def update(self, delta_time):
		self.position += self.velocity
		self.camera.position = self.position + glm.vec3(0, PLAYER_H / 2, 0)
		self.camera.update()