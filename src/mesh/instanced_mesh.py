from src.settings import *
from src.mesh.utils import *
from moderngl_window.opengl.vao import VAO
from src.mesh.base_mesh import Mesh

class InstancedMesh(Mesh):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.max_objects = MAX_OBJECTS_PER_CLUSTER

	def vao_init(self, length):
		self._vao = self.get_vao_instance(self.max_objects * FLOAT32_BYTE_SIZE) # number of bytes to reserve
		print (f'InstancedMesh.{self.name}: VAO created successfully, length of model_list array is {length}')
	
	def update_model_buffer(self, model: glm.mat4x4, index=0):
		if index < self.max_objects:
			# Rewrite data of a specific entity
			model_b = np.array(model.to_list()).astype(np.float32)
			self.model_buffer.write(data=model_b, offset=(index*64))
		else:
			raise ValueError (f'InstancedMesh.{self.name}: ERROR - Model buffer out of range\nMAX_OBJECTS is: {self.max_objects} OBJECT INDEX IS: {index}')