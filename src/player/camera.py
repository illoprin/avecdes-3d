from src.settings import *
from src.shader_program import Shader


class Camera():
	def __init__(self, shader: Shader, pos=(0, 0, 0), rot=(0, 0)) -> None:
		self.position = glm.vec3(pos)
		self.pitch = glm.radians(rot[0])
		self.yaw = glm.radians(rot[1])

		self.forward = DIR_FORWARD
		self.right = DIR_RIGHT
		self.up = DIR_UP

		self.shader = shader

		self.update_vectors()
		self.update_view()
		self.update_projection()

	def update_vectors(self):
		self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
		self.forward.y = glm.sin(self.pitch)
		self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)
		self.forward = glm.normalize(self.forward)
		self.right = glm.normalize(glm.cross(self.forward, DIR_UP))
		self.up = glm.normalize(glm.cross(self.right, self.forward))

	def update_view(self):
		self.view = glm.lookAt(self.position, self.position + self.forward, self.up)
		self.shader.set_byte_data('m_view', self.view)

	def update_projection(self):
		self.projection = glm.perspective(CAM_FOV_H, WIN_ASPECT, CAM_NEAR_FAR[0], CAM_NEAR_FAR[1])
		self.shader.set_byte_data('m_projection', self.projection)

	def update(self):
		self.update_vectors()
		self.update_view()
		

	def move_forward(self, vel):
		self.position += self.forward * vel
	def move_backward(self, vel):
		self.position += -self.forward * vel
	def move_left(self, vel):
		self.position += -self.right * vel
	def move_right(self, vel):
		self.position += self.right * vel
	def move_up(self, vel):
		self.position += DIR_UP * vel
	def move_down(self, vel):
		self.position -= DIR_UP * vel

	def rotate_pitch(self, angle_deg):
		self.pitch += glm.radians(angle_deg)
		self.pitch = glm.clamp(self.pitch, -CAM_MAX_PITCH, CAM_MAX_PITCH)

	def rotate_yaw (self, angle_deg):
		self.yaw += glm.radians(angle_deg)
