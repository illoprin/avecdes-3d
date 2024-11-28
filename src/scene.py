import moderngl as mgl
from src.settings import *
from src.entity.entity import Entity
from src.physics.physics_world import PhysicsWorld

class Scene():
	def __init__(self, app, standart_shader, name: str = 'avecdes'):
		self.name = name
		self.s_program = standart_shader.program
		self.app = app
		self.ctx = app.ctx
		self.objects: list[Entity] = []
		self.physics_world = PhysicsWorld((0, -9.81, 0))
		self.clear_color = (*WIN_CLEAR, 1.0)
		self.init_scene_fbo()
	
	def append_object(self, entity: Entity):
		if entity.program == None and self.s_program != None:
			entity.program = self.s_program
		elif entity.program == None and self.s_program == None:
			return ValueError(f'Scene {self.name} - Main rendering shader not found')
		
		self.physics_world.add(entity)
		self.objects.append(entity)

	def init_scene_fbo(self):
		# Init 3d scene framebuffer
		self.fbo_color = self.ctx.texture(WIN_MODE, components=4)
		self.fbo_depth = self.ctx.depth_renderbuffer(WIN_MODE)
		self.fbo = self.ctx.framebuffer(
			color_attachments=[
				self.fbo_color
			],
			depth_attachment = self.fbo_depth
		)
		print(f'Scene {self.name} - Frame buffer created!')

	def update(self, time=0, delta_time=1):
		# Update physics world
		self.physics_world.update(delta_time)

	def render(self, mode=mgl.TRIANGLES):
		self.fbo.use()
		self.fbo.clear(*self.clear_color)
		[item.render(mode) for item in self.objects]

	def clear(self):
		[item.clear() for item in self.objects]
		self.fbo_color.release()
		self.fbo_depth.release()
		self.fbo.release()
		print(f'Scene {self.name} - Cleared!')