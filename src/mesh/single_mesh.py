from src.settings import *
from src.mesh.utils import *
from moderngl_window.opengl.vao import VAO
from src.mesh.base_mesh import Mesh
from sys import getsizeof

class SingleMesh(Mesh):
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
		self.vao = self.vao_instance()

		print (f'{self.name}: VAO created successfully!')

	def vao_instance(self):
		self.data_buffer = self._ctx.buffer(
			np.hstack((self._vertices, self._texcoords, self._normals), 
			dtype=np.float32)
		)
		attrs = ['in_position', 'in_texcoord_0', 'in_normal']
		format = '3f 2f 3f /v'
		
		self.model_buffer = self.ctx.buffer(reserve=64, dynamic=True)
		vao = self._ctx.vertex_array(self._program,
			[
				(self.data_buffer, format, *attrs),
				(self.model_buffer, '16f /i', 'in_model')
			]
		)
		return vao
	
	def update_model_buffer(self, model: glm.mat4x4):
		matrix = np.array(model.to_list()).astype(np.float32)
		self.model_buffer.write(data=matrix, offset=0)
	
	def render(self, mode):
		self.vao.render(mode, instances=1)

	def clear(self):
		self.data_buffer.release()
		self.vao.release()
		print (f'{self.name}: Cleared!')
