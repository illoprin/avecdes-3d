from src.settings import *
import os

def get_indexed_data(vertices: list, indices, format_size=3, decrement=0, type='f4'):
	vertex_data = np.array(
		[vertices[(index - decrement) * format_size : (index - decrement) * format_size + format_size] for index in indices],
		dtype=type
	)
	return vertex_data

def load_from_obj(path: str):
	file_path = os.path.realpath(f'{ASSETS_DIR}/{path}.obj')
	name: str = ''
	position = []
	normal = []
	texcoord = []

	position_indices = []
	normal_indices = []
	texcoord_indices = []
	if os.path.exists(file_path):
		with open(file_path, 'r') as file:
			for line in file.readlines():
				line_data = line.split(" ")
				if line_data[0] == 'o':
					name = ''.join(filter(str.isalnum, line_data[1]))
				elif line_data[0] == 'v':
					position.append(float(line_data[1]))
					position.append(float(line_data[2]))
					position.append(float(line_data[3]))
				elif line_data[0] == 'vn':
					normal.append(float(line_data[1]))
					normal.append(float(line_data[2]))
					normal.append(float(line_data[3]))
				elif line_data[0] == 'vt':
					texcoord.append(float(line_data[1]))
					texcoord.append(float(line_data[2]))
				elif line_data[0] == 'f':
					for i in range(1, len(line_data)):
						raw_indices = line_data[i].split('/')
						position_indices.append(int(raw_indices[0]))
						texcoord_indices.append(int(raw_indices[1]))
						normal_indices.append(int(raw_indices[2]))
			file.close()
	else:
		print(f"OBJ Loader: ERROR File by path {file_path} is not exists")
		return
	

	print(f"OBJ Loader: Model named {name} loaded successfully")
	return {
		'name': name,
		'position': position,
		'normal': normal,
		'texcoord': texcoord,
		'position_indices': position_indices,
		'normal_indices': normal_indices,
		'texcoord_indices': texcoord_indices
	}