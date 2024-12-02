from src.settings import  *

class Mesh():
	def __init__(self, 
		ctx, 
		program, 
		name='initial_mesh', 
	):
		self._ctx: mgl.Context = ctx
		self._program: mgl.Program = program
		self._name = name

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

	def render(self, mode=mgl.TRIANGLES) -> None: pass

	def clear(self) -> None: pass
