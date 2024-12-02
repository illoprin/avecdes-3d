from src.mesh.instanced_mesh import InstancedMesh
from src.entity.base_entity import BaseEntity
from src.entity.entity import Entity
from src.settings import *

######################
# ---- Instancing ----
# Provides to render multiple simillar objects per one draw call
######################

class EntityCluster():
	def __init__(self, 
		name,
		mesh: InstancedMesh,
		texture: mgl.Texture,
	):
		self._name = name
		self._mesh = mesh
		self._texture = texture
		self._objects: list[Entity] = []

	@property
	def name(self):
		return 'EntityCluster.' + self._name
	
	@property
	def mesh(self):
		return self._mesh
	
	@property
	def objects(self):
		return self._objects
	
	def append_object(self, entity: BaseEntity):
		self._objects.append(entity)

	def __getitem__ (self, index) -> Entity:
		return self._objects[index]
	
	def __setitem__ (self, key, value):
		if isinstance(value, BaseEntity):
			self._objects[key] = value
		else:
			print(f'{self.name}: ERROR - You are trying to assign an object to a cluster that is not an entity!')

	def __len__ (self):
		return len(self._objects)
	
	def process(self):
		self._mesh.vao_init(len(self))
		self.update_buffers()

	def update(self, needs_redraw=False):
		[entity.update() for entity in self._objects]
		self.update_buffers()

	def update_buffers(self):
		for i, entity in enumerate(self._objects):
			if entity.need_redraw:
				self._mesh.update_model_buffer(entity.model, i)
				entity.need_redraw = False

	def render(self, mode):
		self._texture.use(TextureSlot.ClusterDiffuseMap)
		self._mesh.program['u_diffusemap'] = TextureSlot.ClusterDiffuseMap
		self._mesh.render(mode=mode, instances=len(self))

	def clear(self):
		self._objects.clear()
		self._mesh.clear()
		self._texture.release()