import moderngl as mgl
from src.settings import *
from src.entity.base_entity import BaseEntity
from src.master_renderer import MasterRenderer
from src.entity.entity_cluster import EntityCluster
from src.physics.physics_world import PhysicsWorld
from src.light.light_controller import LightController

class Scene():
	def __init__(self, app, shader, name: str = 'avecdes'):
		self._name = name
		self.shader = shader
		self.app = app
		self.clear_color = (*WIN_CLEAR, 1.0)
		self.ctx: mgl.Context = app.ctx

		self.objects: list[BaseEntity] = []
		self.clusters: list[EntityCluster] = []
		self.renderer = MasterRenderer()
		self.physics_world = PhysicsWorld((0, -9.81, 0))
		self.lighting = LightController(app, self.shader)
		self.init_scene_fbo()

	@property
	def name(self):
		return 'Scene.' + self._name
	
	'''
		You can append Entity or prepared EntityCluster to scene
	'''
	def append_object(self, object):
		if isinstance(object, BaseEntity): 
			self.physics_world.add(object)
			self.objects.append(object)
		elif isinstance(object, EntityCluster):
			[self.physics_world.add(entity) for entity in object.objects]
			self.clusters.append(object)

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

		# Колхоз: обновляются все объекты на сцене, как динамические, так и статические
		# Update entities
		[entity.update() for entity in self.objects]

		# Update clusters
		[cluster.update() for cluster in self.clusters]

		# Send dynamic lights data to shader
		self.lighting.update()

	def render(self, mode=mgl.TRIANGLES):
		self.fbo.use()
		self.fbo.clear(*self.clear_color)
		# Send nesserary data  to shader
		self.shader.set_uniform('u_camera_position', self.app.player.camera.position)

		######## Rendering ########
		# Render entity cluster
		self.renderer.render_clusters(self.clusters)
		# Render entities
		self.renderer.render_entities(self.objects)
		###########################
		
				
	def clear(self):
		self.renderer.clear_entities(self.objects)
		self.renderer.clear_clusters(self.clusters)
		self.fbo_color.release()
		self.fbo_depth.release()
		self.fbo.release()
		print(f'{self.name} - Framebuffer cleared')