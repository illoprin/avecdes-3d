from src.settings import *
from src.mesh.utils import *
from moderngl_window.opengl.vao import VAO
from src.mesh.base_mesh import Mesh

class InstancedMesh(Mesh):
	def __init__(self,
		*args,
		# mesh data
		position: np.ndarray = None, 
		normal: np.ndarray = None, 
		texcoord: np.ndarray = None,
		position_indices: np.ndarray = None,
		normal_indices: np.ndarray = None,
		texcoord_indices: np.ndarray = None,
		# needs for example to load obj files
		# start index in AvecdesEngine - 0
		# start index in OBJ in - 1
		decrement: int = 0,
		**kwargs,
	) -> None:
		super().__init__(*args, **kwargs)
		self._vertices = get_indexed_data(position, position_indices, format_size=3, decrement=decrement)
		self._normals = get_indexed_data(normal, normal_indices, format_size=3, decrement=decrement)
		self._texcoords = get_indexed_data(texcoord, texcoord_indices, format_size=2, decrement=decrement)
		self.max_objects = MAX_OBJECTS_PER_CLUSTER

	def vao_init(self, length):
		self._vao = self.instance(self.max_objects) # number of bytes to reserve
		print (f'InstancedMesh.{self.name}: VAO created successfully, length of model_list array is {length}')


	def instance(self, max_objects: int):
		self.data_buffer = self._ctx.buffer(
			np.hstack((self._vertices, self._texcoords, self._normals)).astype(np.float32)
		)
		attrs = ['in_position', 'in_texcoord_0', 'in_normal']
		format = '3f 2f 3f /v'
		
		self.model_buffer = self._ctx.buffer(reserve=(max_objects*64), dynamic=True)
		vao = self._ctx.vertex_array(self._program,
			[
				(self.data_buffer, format, *attrs),
				(self.model_buffer, "16f /i", 'in_model')
			]
		)
		return vao
	
	def update_model_buffer(self, model_list: list[glm.mat4x4]):
		if len(model_list) < self.max_objects:
			# Rewrite data in buffer with actual positions of entites
			self.model_buffer.write(data=self.model_ndarray(model_list), offset=0)
		else:
			raise ValueError (f'InstancedMesh.{self.name}: ERROR - Model buffer out of range\nMAX_OBJECTS is: {self.max_objects} MODEL LIST LEN is: {len(model_list)}')
	
	def render(self, mode, instances):
		self._vao.render(mode=mode, instances=int(instances))

	def clear(self):
		self.model_buffer.release()
		self.data_buffer.release()
		self._vao.release()
		print (f'InstancedMesh.{self.name}: Cleared!')