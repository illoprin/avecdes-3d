from src.settings import *
from src.mesh.utils import *
from moderngl_window.opengl.vao import VAO
from src.mesh.base_mesh import Mesh
from sys import getsizeof

class SingleMesh(Mesh):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self._vao = self.get_vao_instance()
		print (f'{self.name}: VAO created successfully!')
	
	def update_model_buffer(self, model: glm.mat4x4):
		matrix = np.array(model.to_list()).astype(np.float32)
		self.model_buffer.write(data=matrix, offset=0)