from src.settings import *
from src.light.light_types import *
from src.shader_program import Shader

'''
	OUTDATED
'''
def parse_data_to_dict (_dataclass):
	_dict = {}
	for field in fields(_dataclass):
		_dict[field.name] = getattr(_dataclass, field.name)
	return _dict


class LightController():
	def __init__ (self, app, shader: Shader):
		self.app = app
		self.shader = shader

		self.dynamic_lights = []
		self.static_lights = []
		self.sun: SunLight = None
		self.pl_index = 0
		self.sl_index = 0

	def get_shader_name (self, type: LightType):
		if type == LightType.Point:
			return 'point_light'
		if type == LightType.Spot:
			return 'spot_light'
		if type == LightType.Sun:
			return 'sun_light'
		
	def send_light_fields(self, light: Light, is_array=True):
		for field in fields(light):
			if field.name == 'type' or field.name == 'index': continue
			if is_array:
				self.shader.set_uniform(
					f'{self.get_shader_name(light.type)}[{light.index}].{field.name}',
					getattr(light, field.name)
				)
			else:
				self.shader.set_uniform(
					f'{self.get_shader_name(light.type)}.{field.name}',
					getattr(light, field.name)
				)
		

	def update_index(self, light):
		if light.type == LightType.Point:
			light.index = self.pl_index
			self.pl_index += 1
		elif light.type == LightType.Spot:
			light.index = self.sl_index
			self.sl_index += 1
	
	'''
		Add dynamic light
	'''
	def add_dl(self, light: Light):
		if light.type == LightType.Sun or light.type == LightType.Ambient: return
		self.dynamic_lights.append(light)
		self.update_index(light)

	'''
		Add static light
	'''
	def add_sl(self, light: Light):
		if light.type == LightType.Ambient: return
		if light.type == LightType.Sun:
			self.shader.set_uniform('uses_sun_light', 1)
			self.sun = light
			return
		self.static_lights.append(light)
		self.update_index(light)
		self.send_sl_data()
		self.send_sun_data()

	'''
		Add ambient light
	'''
	def add_al(self, light: AmbientLight):
		self.shader.set_uniform('u_ambient_light', light.color)

	def send_sl_data(self):
		for light in self.static_lights:
			self.send_light_fields(light)

	def send_dl_data(self):
		for light in self.dynamic_lights:
			self.send_light_fields(light)

	def send_sun_data(self):
		if not self.sun: return
		self.send_light_fields(self.sun, is_array=False)

	def update(self):
		self.send_dl_data()