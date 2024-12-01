import moderngl as mgl
from src.settings import *
from src.entity.entity import Entity
from src.physics.physics_world import PhysicsWorld
from src.light.light_controller import LightController

class Scene():
	def __init__(self, app, shader, name: str = 'avecdes'):
		self._name = name
		self.s_program = shader.program
		self.app = app
		self.ctx: mgl.Context = app.ctx
		self.objects: list[Entity] = []
		self.physics_world = PhysicsWorld((0, -9.81, 0))
		self.lighting = LightController(app, shader)
		self.clear_color = (*WIN_CLEAR, 1.0)
		self.init_scene_fbo()

	@property
	def name(self):
		return 'Scene.' + self._name
	
	def append_object(self, entity: Entity):
		if entity.program == None and self.s_program != None:
			entity.program = self.s_program
		elif entity.program == None and self.s_program == None:
			return ValueError(f'{self.name} - Main rendering shader not found')
		
		self.physics_world.add(entity)
		self.objects.append(entity)

	def init_scene_fbo(self):
		# Init 3d scene framebuffer
		self.fbo_color = self.ctx.texture(WIN_MODE, components=4, dtype='f4')
		self.fbo_depth = self.ctx.depth_renderbuffer(WIN_MODE)
		self.fbo: mgl.Framebuffer = self.ctx.framebuffer(
			color_attachments=[
				self.fbo_color
			],
			depth_attachment = self.fbo_depth
		)
		print(f'{self.name} - Frame buffer created!')

	@property
	def get_depth_bytes(self):
		return self.fbo.read(attachment=-1)

	def update(self, time=0, delta_time=1):
		# Update physics world
		self.physics_world.update(delta_time)
		# Update only dynamic objects (дикий колхоз на самом деле, но как есть)
		[item.update() for item in self.objects if item.rigidbody != None]
		# Send dynamic lights data to shader
		self.lighting.update()

	def render(self, mode=mgl.TRIANGLES):
		self.fbo.use()
		self.fbo.clear(*self.clear_color)
		# Send nesserary data  to shader
		self.s_program['u_camera_position'].write(self.app.player.camera.position)

		[item.render(mode) for item in self.objects]
		# self.fbo_depth_texture.write(self.get_depth_bytes)

	def clear(self):
		[item.clear() for item in self.objects]
		self.fbo_color.release()
		self.fbo_depth.release()
		self.fbo.release()
		print(f'{self.name} - Framebuffer cleared')