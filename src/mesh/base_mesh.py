from src.settings import  *
from src.mesh.utils import get_indexed_data

class Mesh():
	def __init__(self,
		ctx, 
		program, 
		name='initial_mesh', 
		# mesh data
		position: np.ndarray = None, 
		normal: np.ndarray = None, 
		texcoord: np.ndarray = None,
		position_indices: np.ndarray = None,
		normal_indices: np.ndarray = None,
		texcoord_indices: np.ndarray = None,
		decrement=0
	):
		self._ctx: mgl.Context = ctx
		self._program: mgl.Program = program
		self._name = name

		self._vertices = get_indexed_data(position, position_indices, format_size=3, decrement=decrement)
		self._normals = get_indexed_data(normal, normal_indices, format_size=3, decrement=decrement)
		self._texcoords = get_indexed_data(texcoord, texcoord_indices, format_size=2, decrement=decrement)

		self._vao: mgl.VertexArray = None

	def get_vertices(self):
		return self._vertices
	def get_normals(self):
		return self._normals
	def get_texcoords(self):
		return self._texcoords

	vertices = property(get_vertices)
	normals = property(get_normals)
	texcoords = property(get_texcoords)

	def get_vao_instance(self, reserve=FLOAT32_BYTE_SIZE):
		self.data_buffer = self._ctx.buffer(
			np.hstack((self._vertices, self._texcoords, self._normals)).astype(np.float32)
		)
		attrs = ['in_position', 'in_texcoord_0', 'in_normal']
		format = '3f 2f 3f /v'
		
		self.model_buffer = self._ctx.buffer(reserve=reserve, dynamic=True)
		vao = self._ctx.vertex_array(self._program,
			[
				(self.data_buffer, format, *attrs),
				(self.model_buffer, "16f /i", 'in_model')
			]
		)
		return vao

	@property
	def name(self): return 'Mesh.' + self._name
	
	@property
	def ctx(self) -> mgl.Context: return self._ctx

	@property
	def program(self) -> mgl.Program: return self._program

	def model_ndarray(self, list: list[glm.mat4x4]) -> np.ndarray:
		models = []
		for mat in list:
			models.append(np.hstack(mat.to_list()))
		models = np.array(models).astype(np.float32)
		return models
	
	def instance(self) -> mgl.VertexArray: pass

	def render(self, mode=mgl.TRIANGLES, instances=1) -> None:
		self._vao.render(mode, instances=instances)

	def clear(self) -> None:
		self.model_buffer.release()
		self.data_buffer.release()
		self._vao.release()
		print (f'{self.name}: Cleared!')