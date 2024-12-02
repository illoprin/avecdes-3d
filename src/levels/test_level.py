from src.scene import Scene
from src.entity.entity import Entity
from src.entity.entity_cluster import EntityCluster
import moderngl_window.geometry as mglg
from src.settings import *
from src.mesh.mesh_types import init_cube_mesh, init_zombie_mesh_i
from src.physics.aabb import AABB
from src.texture import TextureManager
from src.light.light_types import PointLight, AmbientLight, SpotLight



class TestLevel(Scene):
	def __init__ (self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		cube_mesh = init_cube_mesh(self.ctx, self.shader)

		# Init meshes
		zombie_mesh = init_zombie_mesh_i(self.ctx, self.shader)
		zombie_diff = TextureManager.load_texture(self.ctx, 'textures/zombie', False, mgl.NEAREST)

		# Init textures
		checker = TextureManager.load_texture(self.ctx, 'textures/checker', False, mgl.NEAREST)
		# wood = TextureManager.load_texture(self.ctx, 'textures/wood', False, mgl.NEAREST)

		# Create zombies
		self.zombie_cluster = EntityCluster('zombies', zombie_mesh, zombie_diff)
		grid_x = 10
		grid_y = 10
		size = 3
		for i in range(grid_x * grid_y):
			x = (i % 10 * size) - (grid_x / 2)
			y = (i // 10 * size) - (grid_y / 2)
			zombie = Entity(
				mesh='root',
				texture='root',
				name='zombie',
				pos=(x, 0, y),
				scl=(2, 2, 2)
			)
			self.zombie_cluster.append_object(zombie)
		self.zombie_cluster.process()
		
		# Append objects to scene
		self.append_object(self.zombie_cluster)
		self.ground = Entity(
			mesh=cube_mesh,
			name='ground',
			texture=checker,
			pos=(0, -.25, 0),
			scl=(20, .25, 20),
		)
		self.append_object(self.ground)

		# Init lights
		self.lighting.add_al(
			AmbientLight(color=glm.vec3(0.1/4, 0.11/4, 0.13/4))
		)
		self.lighting.add_sl(
			PointLight(position=glm.vec3(-3, 4, 4), color=glm.vec3(.8, .65, .3))
		)
		self.blue_light = PointLight(
			position=glm.vec3(4, 2, -3), color=glm.vec3(.3, .3, .75)
		)
		self.lighting.add_dl(self.blue_light)
		self.flashlight = SpotLight(
			position=glm.vec3(2, 4,-5),
			direction=glm.vec3(0, -1, 0),
			color=glm.vec3(.9, .93, .98),
		)
		self.lighting.add_dl(self.flashlight)


	def update(self, time=0, delta_time=1):
		# Update objects
		#################
		self.zombie_cluster[36].position = glm.vec3(
			self.zombie_cluster[36].position.x,
			glm.sin(time) * 3,
			self.zombie_cluster[36].position.z
		)
		# Update lights
		#################
		self.blue_light.position += glm.vec3(glm.sin(time)*1.5, 0, glm.cos(time)*1.5) * delta_time
		self.flashlight.position = self.app.player.camera.position
		self.flashlight.direction = self.app.player.camera.forward
		# Update parent
		super().update(time, delta_time)