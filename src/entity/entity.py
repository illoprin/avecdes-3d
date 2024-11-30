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
		texture=None,
		collider='none',
		use_physics=False,
		gravity=False,
		name='defaultEntity'
	):
		self._name = name
		self.vao = vao
		self.program = program
		# Transforms
		self.position = glm.vec3(pos)
		self.rotation = glm.vec3(rot)
		self.scale = glm.vec3(scl)
		self.update()
		# Texturing
		self.texture_filter_type = mgl.LINEAR
		self.texture = None if not texture else TextureManager.load_texture(vao.ctx, texture, False, mgl.NEAREST)
		# Physics
		self.rigidbody = None
		self.collider = Collider()
		if collider == 'aabb' and (not use_physics):
			self.collider = AABB(self)
			self.rigidbody = None
			print (f'Entity: {self.name} - Added AABB collider')
		elif collider == 'aabb' and use_physics:
			self.collider = AABB(self)
			self.rigidbody = Rigidbody(use_gravity=gravity)
			print (f'Entity: {self.name} - Added rigidbody and AABB collider')
	
	@property
	def name(self):
		return f'Entity.{self._name}'

	@property
	def has_rigidbody(self):
		return self.rigidbody != None

	def set_model(self, pos, rot, scl):
		model = glm.mat4x4(1.0)
		model = glm.scale(model, scl)
		pitch, yaw, roll = rot
		model = glm.rotate(model, glm.radians(pitch), (1, 0, 0))
		model = glm.rotate(model, glm.radians(yaw), (0, 1, 0))
		model = glm.rotate(model, glm.radians(roll), (0, 0, 1))
		model = glm.translate(model, pos)
		self.model = model
	
	def rotate(self, rotation=(0, 0, 0)):
		pitch, yaw, roll = rotation
		self.model = glm.rotate(self.model, glm.radians(pitch), (1, 0, 0))
		self.model = glm.rotate(self.model, glm.radians(yaw), (0, 1, 0))
		self.model = glm.rotate(self.model, glm.radians(roll), (0, 0, 1))
		self.rotation += glm.vec3(rotation)

	def resize(self, scale=(1, 1, 1)):
		self.model = glm.scale(self.model, glm.vec3(scale))
		self.scale *= glm.vec3(scale)

	def transform(self, transform=(0, 0, 0)):
		self.model = glm.translate(self.model, glm.vec3(transform))
		self.position += glm.vec3(transform)

	def update(self):
		self.set_model(self.position, self.rotation, self.scale)

	def render(self, mode=mgl.TRIANGLES):
		self.texture.use(TextureSlot.DiffuseMap)
		self.program['u_texture'] = TextureSlot.DiffuseMap
		self.program['m_model'].write(self.model)
		self.vao.render(self.program, mode)

	def clear(self):
		self.vao.release()
		self.texture.release()