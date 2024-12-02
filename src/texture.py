from PIL import Image
from src.settings import *
import os

class TextureManager:
	def __init__(self, ctx: mgl.Context) -> None:
		self.ctx = ctx

	@staticmethod
	def load_texture(ctx, assets_path: str, alpha=False, filter_type=0x2601) -> mgl.Texture:
		path = f'{ASSETS_DIR}/{assets_path}.png'
		if os.path.isfile(path):
			components = 4 if alpha else 3
			format = 'RGBA' if alpha else 'RGB'
			#
			img = Image.open(path).convert(format)
			texture = ctx.texture(size=img.size, components=components, data=img.tobytes(), dtype='f1')
			texture.filter = (filter_type, filter_type)
		else:
			print (f'TextureManager: {assets_path} is not exists')
			return

		print (f'TextureManager: {assets_path} texture loaded successfully')
		return texture