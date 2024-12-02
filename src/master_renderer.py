from src.entity.entity_cluster import EntityCluster
from src.entity.entity import Entity
from src.mesh.base_mesh import Mesh
from src.settings import *

class MasterRenderer():
	def __init__ (self):
		self.mode = mgl.TRIANGLES

	def render_entities(self, entity_list: list[Entity]):
		for entity in entity_list:
			entity.texture.use(TextureSlot.DiffuseMap)
			entity.mesh.program['u_diffusemap'] = TextureSlot.DiffuseMap
			entity.mesh.update_model_buffer(entity.model)
			entity.mesh.render(self.mode)

	def render_clusters(self, cluster_list: list[EntityCluster]):
		[cluster.render(self.mode) for cluster in cluster_list]
			
	def clear_entities(self, entity_list: list[Entity]):
		meshes: list[Mesh] = []
		textures: list[mgl.Texture] = []

		# Collect all unique meshes and textures
		for entity in entity_list:
			entity.clear()
			print (f'MasterRenderer: {entity.name} Cleared')
			if not entity.mesh in meshes:
				meshes.append(entity.mesh)
			if not entity.texture in textures:
				textures.append(entity.texture)

		# Clear meshes
		for mesh in meshes:
			mesh.clear()
		
		# Clear textures
		for texture in textures:
			texture.release()

	def clear_clusters(self, cluster_list: list[EntityCluster]):
		[cluster.clear() for cluster in cluster_list]