from src.settings import *
from src.physics.aabb import AABB
from src.physics.physics_engine import *
from src.physics.rigidbody import Rigidbody
from src.mesh.single_mesh import SingleMesh
from src.mesh.instanced_mesh import InstancedMesh
from src.entity.base_entity import BaseEntity


class Entity(BaseEntity):
	def __init__(self,
		*args,
		mesh=None,
		texture=None,
		collider='none',
		use_physics=False,
		gravity=False,
		**kwargs,
	):
		super().__init__(*args, **kwargs)
		#
		# Mesh link init
		if isinstance(mesh, SingleMesh) or mesh == 'root': self.mesh = mesh
		else: raise ValueError(f'{self.name}: ERROR - Invalid mesh object assigned')
		#
		# Texture link init
		if isinstance(texture, mgl.Texture) or texture == 'root': self.texture = texture
		else: raise ValueError(f'{self.name}: ERROR - Invalid texture object assigned') 
		#
		# Physics
		self.rigidbody = None
		self.collider = Collider()
		if collider == 'aabb' and (not use_physics):
			self.collider = AABB(self)
			self.rigidbody = None
			print (f'{self.name}: Added AABB collider')
		elif collider == 'aabb' and use_physics:
			self.collider = AABB(self)
			self.rigidbody = Rigidbody(use_gravity=gravity)
			print (f'{self.name}: Added rigidbody and AABB collider')
		
	@property
	def has_rigidbody(self):
		return self.rigidbody != None