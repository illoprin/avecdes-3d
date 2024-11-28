from src.scene import Scene
from src.entity.entity import Entity
import moderngl_window.geometry as mglg
from src.settings import *



class TestLevel(Scene):
	def __init__ (self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		cube_vao = mglg.cube()
		self.cube_e = Entity(vao=cube_vao, texture='textures/checker', pos=(0, 0, 0))
		self.append_object(self.cube_e)
		self.append_object(Entity(
			cube_vao, 
			texture='textures/checker', 
			pos=(0, 4, 0),
			scl=(10, .5, 10)
		))
		self.append_object(Entity(
			cube_vao, 
			texture='textures/checker', 
			pos=(-5, 0, 0),
			scl=(.5, 3, 5)
		))
		self.append_object(Entity(
			cube_vao,
			texture='textures/checker', 
			pos=(5, 0, 0),
			scl=(.5, 3, 5)
		))
		self.clear_color = ([0.0]*4)

		

	def update(self, time=0, delta_time=1):
		# Update objects
		player_position = self.app.player.camera.position
		delta = player_position - self.cube_e.position
		player_dir = glm.vec3(0.0) if glm.length(delta) <= 2 else glm.normalize(delta) * delta_time * 5
		self.cube_e.transform(player_dir)
		# Super update physics world
		super().update(time, delta_time)