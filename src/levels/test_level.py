from src.settings import *
from src.scene import Scene
from src.entity.entity import Entity
from src.texture import TextureManager
from src.entity.entity_cluster import EntityCluster
from src.light.light_types import PointLight, AmbientLight, SpotLight

# TESTING - LOADING MESH DATA
from src.mesh.utils import load_from_obj
from src.mesh.single_mesh import SingleMesh

class TestLevel(Scene):
	def __init__ (self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Init objs
		# dl - demo level
		boxes_mesh_data = load_from_obj('levels/demo_level/boxes')
		bushes_mesh_data = load_from_obj('levels/demo_level/bushes')
		ground_mesh_data = load_from_obj('levels/demo_level/ground')
		tree_branches_mesh_data = load_from_obj('levels/demo_level/tree_branches')
		tree_foliage_mesh_data = load_from_obj('levels/demo_level/tree_foliage')

		# Init meshes
		dl_boxes_mesh = SingleMesh(
							ctx=self.ctx, program=self.shader.program,
							position=boxes_mesh_data['position'],
							position_indices=boxes_mesh_data['position_indices'],
							normal=boxes_mesh_data['normal'],
							normal_indices=boxes_mesh_data['normal_indices'],
							texcoord=boxes_mesh_data['texcoord'],
							texcoord_indices=boxes_mesh_data['texcoord_indices'],
							decrement=1,
							name='dl_boxes_mesh'
						)
		dl_ground_mesh = SingleMesh(
							ctx=self.ctx, program=self.shader.program,
							position=ground_mesh_data['position'],
							position_indices=ground_mesh_data['position_indices'],
							normal=ground_mesh_data['normal'],
							normal_indices=ground_mesh_data['normal_indices'],
							texcoord=ground_mesh_data['texcoord'],
							texcoord_indices=ground_mesh_data['texcoord_indices'],
							decrement=1,
							name='dl_ground_mesh'
						)
		dl_bushes_mesh = SingleMesh(
							ctx=self.ctx, program=self.shader.program,
							position=bushes_mesh_data['position'],
							position_indices=bushes_mesh_data['position_indices'],
							normal=bushes_mesh_data['normal'],
							normal_indices=bushes_mesh_data['normal_indices'],
							texcoord=bushes_mesh_data['texcoord'],
							texcoord_indices=bushes_mesh_data['texcoord_indices'],
							decrement=1,
							name='dl_bushes_mesh',
							cull_face=False
						)
		dl_branches_mesh = SingleMesh(
							ctx=self.ctx, program=self.shader.program,
							position=tree_branches_mesh_data['position'],
							position_indices=tree_branches_mesh_data['position_indices'],
							normal=tree_branches_mesh_data['normal'],
							normal_indices=tree_branches_mesh_data['normal_indices'],
							texcoord=tree_branches_mesh_data['texcoord'],
							texcoord_indices=tree_branches_mesh_data['texcoord_indices'],
							decrement=1,
							name='dl_bushes_mesh'
						)
		dl_leaves_mesh = SingleMesh(
							ctx=self.ctx, program=self.shader.program,
							position=tree_foliage_mesh_data['position'],
							position_indices=tree_foliage_mesh_data['position_indices'],
							normal=tree_foliage_mesh_data['normal'],
							normal_indices=tree_foliage_mesh_data['normal_indices'],
							texcoord=tree_foliage_mesh_data['texcoord'],
							texcoord_indices=tree_foliage_mesh_data['texcoord_indices'],
							decrement=1,
							name='dl_bushes_mesh'
						)
		# Init textures
		ground_texture = TextureManager.load_texture(self.ctx, 'textures/grass', False, mgl.NEAREST)
		bush_texture = TextureManager.load_texture(self.ctx, 'textures/bush', True, mgl.NEAREST)
		wood_texture = TextureManager.load_texture(self.ctx, 'textures/wood', False, mgl.NEAREST)
		leaves_texture = TextureManager.load_texture(self.ctx, 'textures/tree_leave', True, mgl.NEAREST)
		box_texture = TextureManager.load_texture(self.ctx, 'textures/box', False, mgl.NEAREST)

		# Create bushes
		self.dl_bushes = Entity(
			mesh=dl_bushes_mesh,
			name='dl_bushes',
			texture=bush_texture,
			collider='none',
		)
		# Create ground
		self.dl_ground = Entity(
			mesh=dl_ground_mesh,
			name='dl_ground',
			texture=ground_texture,
			collider='none',
		)
		# Create boxes
		self.dl_boxes = Entity(
			mesh=dl_boxes_mesh,
			name='dl_boxes',
			texture=box_texture,
			collider='none',
		)
		# Create tree foliage entity
		self.dl_foliage = Entity(
			mesh=dl_leaves_mesh,
			name='dl_foliage',
			texture=leaves_texture,
			collider='none'
		)
		# Create tree branches entity
		self.dl_branches = Entity(
			mesh=dl_branches_mesh,
			name='dl_branches',
			texture=wood_texture,
			collider='none'
		)

		# Append objects to scene
		self.append_object(self.dl_bushes)
		self.append_object(self.dl_ground)
		self.append_object(self.dl_boxes)
		self.append_object(self.dl_branches)
		self.append_object(self.dl_foliage)
		
		# Init lights
		self.lighting.add_al(
			AmbientLight(color=glm.vec3(0.1/9, 0.11/9, 0.13/9))
		)
		# Init flashlight
		self.flashlight = SpotLight()
		self.lighting.add_dl(self.flashlight)

		# Init static lights
		self.lighting.add_sl(PointLight(
			position=glm.vec3(4.19, 0.330, 4.66), color=glm.vec3(0.9, 0.20, 0.34), intensity=4.0, radius=14.35
		))
		self.lighting.add_sl(SpotLight(
			position=glm.vec3(-6.837, -0.19, 1.466), direction=glm.vec3(0.38, -.37, -.83),
			intensity=float(10.2), distance=float(8.3)
		))

		# Init dynamic lights
		self.orange_light = PointLight(color=glm.vec3(.97, .54, .05), position=glm.vec3(1.4, 0.69, -1.13))
		self.blue_light = PointLight(color=glm.vec3(.18, .6, .94), position=glm.vec3(1.5, 0.71, -5))
		self.lighting.add_dl(self.orange_light)
		self.lighting.add_dl(self.blue_light)


	def update(self, time=0, delta_time=1):
		# Update objects
		#################

		# Update lights
		#################
		self.orange_light.position.z = -3.02 - glm.sin(time)
		self.blue_light.position.x = 0.18 + glm.cos(time)
		fl_pos = self.app.player.camera.position
		fl_dir = self.app.player.camera.forward
		self.flashlight.position = fl_pos
		self.flashlight.direction = fl_dir
		# Update parent
		super().update(time, delta_time)
