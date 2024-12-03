from src.settings import *
from src.scene import Scene
from src.entity.entity import Entity
from src.texture import TextureManager
from src.entity.entity_cluster import EntityCluster
from src.mesh.mesh_types import init_cube_mesh, init_zombie_mesh_i, init_cube_mesh_i
from src.light.light_types import PointLight, AmbientLight, SpotLight

class TestLevel(Scene):
	def __init__ (self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Init meshes
		cube_mesh_ins = init_cube_mesh_i(self.ctx, self.shader)
		cube_mesh = init_cube_mesh(self.ctx, self.shader)

		# Init textures
		checker = TextureManager.load_texture(self.ctx, 'textures/checker', False, mgl.NEAREST)
		wood = TextureManager.load_texture(self.ctx, 'textures/wood', False, mgl.NEAREST)

		# Create zombies
		self.cube_cluster = EntityCluster('cubes', cube_mesh_ins, checker)
		grid_x = 4
		grid_y = 4
		size = 4
		for i in range(grid_x * grid_y):
			x = ((i % grid_x) - (grid_x / 2)) * size
			y = ((i // grid_y) - (grid_y / 2)) * size
			cube = Entity(
				mesh='root',
				texture='root',
				name='instanced_cube',
				collider='aabb',
				use_physics=True,
				gravity=True,
				pos=(x + np.random.random(), 10, y + np.random.random()),
				origin=(0, 1, 0)
			)
			# Append objects to cluster
			self.cube_cluster.append_object(cube)
		self.cube_cluster.process()
		self.ground = Entity(
			mesh=cube_mesh,
			name='ground',
			texture=wood,
			collider='aabb',
			pos=(0, -1, 0),
			scl=(20, .5, 20),
			origin=(0, 1, 0)
		)
		# Append objects to scene
		self.append_object(self.cube_cluster)
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
		# print (self.cube_cluster[0].rigidbody.grounded, self.cube_cluster[0].rigidbody.acceleration)
		# Update lights
		#################
		self.blue_light.position += glm.vec3(glm.sin(time)*1.5, 0, glm.cos(time)*1.5) * delta_time
		self.flashlight.position = self.app.player.camera.position
		self.flashlight.direction = self.app.player.camera.forward
		# Update parent
		super().update(time, delta_time)