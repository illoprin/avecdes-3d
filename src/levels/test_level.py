from src.scene import Scene
from src.entity.entity import Entity
import moderngl_window.geometry as mglg
from src.settings import *



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

	def update(self, time=0, delta_time=1):
		# Update objects
		player_position = self.app.player.camera.position
		delta = player_position - self.cube_e.position
		self.cube_e.rigidbody.add_force(delta)
		# Update parent
		super().update(time, delta_time)