from src.settings import *

def get_indexed_data(vertices: list, indices, format_size=3, decrement=0, type='f4'):
	vertex_data = np.array(
		[vertices[(index - decrement) * format_size : (index - decrement) * format_size + format_size] for index in indices],
		dtype=type
	)
	return vertex_data