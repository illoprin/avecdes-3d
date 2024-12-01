from src.scene import Scene
from src.entity.entity import Entity
import moderngl_window.geometry as mglg
from src.settings import *
from src.light.light_types import PointLight, AmbientLight, SpotLight



class TestLevel(Scene):
	def __init__ (self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		cube_vao = mglg.cube()
		self.cube_e = Entity(
			vao=cube_vao, 
			texture='textures/checker', 
			pos=(0, 2, 5),
			collider='aabb',
			use_physics=True,
			name='top'
		)
		self.append_object(self.cube_e)

		self.append_object(Entity(
			vao=cube_vao, 
			texture='textures/checker', 
			pos=(-.2, 4, 0),
			collider='aabb',
			use_physics=True,
			gravity=True,
			name='bottom'
		))
		self.append_object(Entity(
			vao=cube_vao, 
			texture='textures/checker', 
			pos=(0, 5, 0),
			collider='aabb',
			use_physics=True,
			gravity=True,
			name='RandomCubes'
		))
		# self.append_object(Entity(
		# 	vao=cube_vao, 
		# 	texture='textures/checker', 
		# 	pos=(-2, 7, -.3),
		# 	collider='aabb',
		# 	use_physics=True,
		# 	gravity=True,
		# 	name='RandomCubes'
		# ))

		self.append_object(Entity(
			cube_vao, 
			texture='textures/wood',
			pos=(0, 0, 0),
			scl=(10, 0.5, 10),
			collider='aabb',
			name='ground'
		))
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
		##### Init spotlight #####
		self.flashlight = SpotLight(
			position=glm.vec3(2, 4,-5),
			direction=glm.vec3(0, -1, 0),
			color=glm.vec3(.9, .93, .98),
		)
		self.lighting.add_dl(self.flashlight)


	def update(self, time=0, delta_time=1):
		# Update objects
		player_position = self.app.player.camera.position
		delta = player_position - self.cube_e.position
		self.cube_e.rigidbody.add_force(delta)
		# Update lights
		self.blue_light.position += glm.vec3(glm.sin(time)*1.5, 0, glm.cos(time)*1.5) * delta_time
		self.flashlight.position = self.app.player.camera.position
		self.flashlight.direction = self.app.player.camera.forward
		# Update parent
		super().update(time, delta_time)