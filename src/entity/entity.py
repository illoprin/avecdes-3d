from src.settings import *
from src.texture import TextureManager
from src.physics.physics_engine import *
from src.physics.aabb import AABB
from src.physics.rigidbody import Rigidbody

class Entity():
	def __init__(self,
		vao, 
		program: mgl.Program = None, 
		pos=(0,0,0), 
		rot=(0,0,0), 
		scl=(1,1,1), 
		model=glm.mat4x4(1.0), 
		texture=None,
		collider='none',
		use_physics=False,
		name='defaultEntity'
	):
		self.name = name
		self.vao = vao
		self.program = program
		# Transforms
		self.position = glm.vec3(pos)
		self.rotation = glm.vec3(rot)
		self.scale = glm.vec3(scl)
		self.model = model
		# Applying transforms
		self.transform(pos)
		self.rotate(rot)
		self.resize(scl)
		# Texturing
		self.texture_filter_type = mgl.LINEAR
		self.texture = None if not texture else TextureManager.load_texture(vao.ctx, texture, False, mgl.LINEAR)
		# Physics
		if not collider == 'none':
			self.collider = AABB(self)
		elif not collider == 'none' and use_physics:
			self.collider = AABB(self)
			self.rigidbody = Rigidbody()
		else:
			self.collider = Collider()
			self.rigidbody = None

	def rotate(self, rotation=(0, 0, 0)):
		pitch, yaw, roll = rotation
		self.model = glm.rotate(self.model, glm.radians(pitch), (1, 0, 0))
		self.model = glm.rotate(self.model, glm.radians(yaw), (0, 1, 0))
		self.model = glm.rotate(self.model, glm.radians(roll), (0, 0, 1))
		self.rotation += glm.vec3(rotation)

	def resize(self, scale=(1, 1, 1)):
		self.model = glm.scale(self.model, scale)
		self.scale *= glm.vec3(scale)

	def transform(self, transform=(0, 0, 0)):
		self.model = glm.translate(self.model, transform)
		self.position += glm.vec3(transform)

	def render(self, mode=mgl.TRIANGLES):
		self.texture.use(1)
		self.program['u_texture'] = 1
		self.program['m_model'].write(self.model)
		self.vao.render(self.program, mode)

	def clear(self):
		self.vao.release()
		self.texture.release()