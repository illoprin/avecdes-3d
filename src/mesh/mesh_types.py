CUBE = {
    'position': [
        # x, y, z
        -.5, -.5, .5,
        .5, -.5, .5,
        -.5, .5, .5,
        .5, .5, .5,
        -.5, -.5, -.5,
        .5, -.5, -.5,
        -.5, .5, -.5,
        .5, .5, -.5
    ],
    'texcoord': [
        0, 0,
        1, 0,
        1, 1,
        0, 1
    ],
	'normal': [
		0, 1, 0,
		0, -1, 0,
		-1, 0, 0,
		1, 0, 0,
		0, 0, -1,
		0, 0, 1
	],
	'normal_indices': [
		# top
		0, 0, 0,
		0, 0, 0,
		# bottom
		1, 1, 1,
		1, 1, 1,
		# left
		2, 2, 2,
		2, 2, 2,
		# right
		3, 3, 3,
		3, 3, 3,
		# front
		4, 4, 4,
		4, 4, 4,
		# back
		5, 5, 5,
		5, 5, 5,
	],
    'texcoord_indices': [
        # top
        2, 3, 0,
        2, 0, 1,
        # bottom
        0, 1, 2,
        0, 2, 3,
        # left
        2, 3, 0,
        2, 0, 1,
        # right
        2, 3, 0,
        2, 0, 1,
        # front
        2, 3, 0,
        0, 1, 2,
        # back
        2, 3, 0,
        2, 0, 1
    ],
    'position_indices': [
        # top
        7, 6, 2,
        7, 2, 3,
        # bottom
        1, 0, 4,
        1, 4, 5,
        # left
        2, 6, 4,
        2, 4, 0,
        # right
        7, 3, 1,
        7, 1, 5,
        # front
        3, 2, 0,
        0, 1, 3,
        # back
        6, 7, 5,
        6, 5, 4
    ]
}

PYRAMID = {
    'position':[
        0, 0, 1,
        0, 0, 0,
        1, 0, .5,
        .5, 1, .5
    ],
    'position': [
        # front
        3, 2, 1,

        # left
        3, 1, 0,

        # right
        2, 3, 0,

        # bottom
        0, 1, 2
    ],
    'texcoord': [
        0, 0,
        1, 0,
        .5, 1,
    ],
    'texcoord_indices': [
        # left
        2, 1, 0,
        # right
        2, 1, 0,
        # back
        2, 1, 0,
        # bottom
        0, 2, 1
    ]
}

AXIS = {
    'vertices': [
        0, 0, 0,
        1, 0, 0,
        0, 1, 0,
        0, 0, 1
    ],

    'indices': [
        # X
        0, 1,
        # Y
        0, 2,
        # Z
        0, 3,
    ],

    'color_indices': [
        # X
        1, 1,
        # Y
        2, 2,
        # Z
        3, 3,
    ],

    'color': [
        0, 0, 0,
        # X
        1, 0, 0,
        # Y
        0, 1, 0,
        # Z
        0, 0, 1
    ]
}


from src.mesh.instanced_mesh import InstancedMesh
from src.mesh.single_mesh import SingleMesh
from src.mesh.utils import *
from src.settings import *


def init_cube_mesh(ctx, shader):
    return SingleMesh(
        ctx = ctx,
        program = shader.program,
        position = CUBE['position'],
        position_indices = CUBE['position_indices'],
        normal = CUBE['normal'],
        normal_indices = CUBE['normal_indices'],
        texcoord = CUBE['texcoord'],
        texcoord_indices = CUBE['texcoord_indices'],
        decrement=0,
        name='cube'

    )

def init_cube_mesh_i(ctx, shader):
    return InstancedMesh(
        ctx = ctx,
        program = shader.program,
        position = CUBE['position'],
        position_indices = CUBE['position_indices'],
        normal = CUBE['normal'],
        normal_indices = CUBE['normal_indices'],
        texcoord = CUBE['texcoord'],
        texcoord_indices = CUBE['texcoord_indices'],
        decrement=0,
        name='cube_instanced'
    )

def init_zombie_mesh_i(ctx, shader):
    ZOMBIE = load_from_obj('obj/zombie')
    return InstancedMesh(
        ctx = ctx,
        program = shader.program,
        position = ZOMBIE['position'],
        position_indices = ZOMBIE['position_indices'],
        normal = ZOMBIE['normal'],
        normal_indices = ZOMBIE['normal_indices'],
        texcoord = ZOMBIE['texcoord'],
        texcoord_indices = ZOMBIE['texcoord_indices'],
        decrement=1,
        name=ZOMBIE['name']
    )
        