
from PIL import Image
import moderngl_window as mglw
import moderngl_window.geometry as mglg

import os
from datetime import datetime

from src.settings import *
from src.shader_program import Shader
from src.player.player import Player
from src.levels.test_level import TestLevel

class SimplexEngine(mglw.WindowConfig):
	gl_version = (4, 3)
	window_size = WIN_MODE
	title = WIN_TITLE
	resizable = False
	vsync = False

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.ctx.enable(OPENGL_STATEMENTS)

		# Init base vars
		self.time = 0
		self.delta_time = 1
		self.fps = 0
		# Create help folders
		self.create_dirs()

		self.init_scene()

		self.init_screen()

		self.update_window()

	def init_scene(self):
		self.scene_light_shader = Shader(self.ctx, 'd_light')
		self.player = Player(self.wnd, self.scene_light_shader, pos=(0, 0, -2))
		self.scene = TestLevel(self, self.scene_light_shader, 'test_level')
		
	def update_scene(self):
		if self.wnd.mouse_exclusivity:
			self.player.movement(self.delta_time)
		self.player.update(self.delta_time)

		# update scene
		self.scene.update(self.time, self.delta_time)
		

	def render_scene(self):
		self.scene.render()

	def init_screen(self):
		# Load screen shader
		self.screen_shader = Shader(self.ctx, 'screen')
		self.screen_vao = mglg.quad_2d(normals=False)

	def combine_fbos(self):
		# COMBINING FBOS
		# Use main screen framebuffer
		self.ctx.screen.use()
		self.ctx.screen.clear(0, 0, 0, 1.0)
		# Use texture of 3d scene framebuffer
		self.scene.fbo_color.use(TextureSlot.SceneColorBuffer)
		# User scene depth texture
		# self.scene.fbo_depth_texture.use(SCENE_DEPTH_FRAMEBUFFER)
		# Send this texture to the screen shader
		self.screen_shader.set_uniform('scene_view', TextureSlot.SceneColorBuffer)
		# Render fullscreen quad
		self.screen_vao.render(mode=mgl.TRIANGLES, program=self.screen_shader.program)

	def update_window(self):
		period = math.ceil(self.time*1000) % 1000
		if period == 0:
			self.wnd.title = f'{WIN_TITLE} | FPS: {self.fps: .0f}'
		# self.screen_shader.set_uniform('u_width', WIN_MODE[0])
		# self.screen_shader.set_uniform('u_height', WIN_MODE[1])
			
	def render(self, time: float, frame_time: float):
		self.time = time
		self.delta_time = frame_time
		self.fps = 1 / self.delta_time
		self.update_window()
		self.update_scene()
		self.render_scene()
		self.combine_fbos()

	def create_dirs(self):
		if not os.path.isdir(SCREENSHOTS_DIR):
			os.mkdir(SCREENSHOTS_DIR)
			print (f'Avecdes 3D: /{SCREENSHOTS_DIR} folder created')
		if not os.path.isdir(CACHE_DIR):
			os.mkdir(CACHE_DIR)
			print (f'Avecdes 3D: /{CACHE_DIR} folder created')

	def take_screenshot(self):
		_data = self.ctx.screen.read(components=3) # COLOR
		file_path = f'{SCREENSHOTS_DIR}/{datetime.now().strftime("%d-%m-%YT%H_%M-%S")}.png'
		Image.frombytes('RGB', WIN_MODE, data=_data).transpose(Image.FLIP_TOP_BOTTOM).save(
			file_path,
			format='PNG',
			quality=80
		)
	
	##### HANDLE INPUT EVENTS #####
	def key_event(self, key, action, modifiers):
		self.player.handle_keyboard(key, action, modifiers)
		if action == self.wnd.keys.ACTION_PRESS:
			if key == self.wnd.keys.TAB:
				self.wnd.mouse_exclusivity = not self.wnd.mouse_exclusivity
			if key == self.wnd.keys.F5:
				self.take_screenshot()
	def mouse_drag_event(self, x: int, y: int, dx: int, dy: int):
		pass
	def mouse_position_event(self, x: int, y: int, dx: int, dy: int):
		if self.wnd.mouse_exclusivity:
			self.player.handle_mouse(dx, dy)
	###############################

	def close(self):
		# Clear scene
		self.scene_light_shader.clear()
		self.scene.clear()

		# Clear screen
		self.screen_vao.release()
		self.screen_shader.clear()
		self.ctx.release()
