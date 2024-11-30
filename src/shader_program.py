from src.settings import *

class Shader():
	def __init__(self, ctx: mgl.Context, name: str):
		self.ctx = ctx
		self.name = name
		
		# Read vertex shader program
		with open(f'{SHADER_DIR}/{name}.vert', 'r') as file:
			vertex_shr = file.read()

		# Read fragment shader program
		with open(f'{SHADER_DIR}/{name}.frag', 'r') as file:
			fragment_shr = file.read()

		self.program = self.ctx.program(vertex_shader=vertex_shr, fragment_shader=fragment_shr)
		print (f'Shader program {self.name} - Loaded!')

	def set_byte_data(self, uniform_name: str, value: any):
		self.program[uniform_name].write(value)

	def set_uniform(self, uniform_name: str, value):
		self.program[uniform_name] = value

	def clear(self):
		self.program.release()
		print (f'Shader program {self.name} - Released!')