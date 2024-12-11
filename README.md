# Avecdes 3D Engine

3D Engine on Python (renderer, physics)

> [!TIP]
> **Controls**<br>
> W/A/S/D - Movement<br>
> Ctrl - acceleration<br>
> F - toggle flashlight<br>
> F5 - take screenshot<br>

![11-12-2024T17_49-07](https://github.com/user-attachments/assets/cda7c742-58d4-4e46-86b7-090d1c192d7f)

![11-12-2024T17_49-23](https://github.com/user-attachments/assets/02b44032-958a-46a5-8900-62187f5abc67)

![screenshot_2](https://github.com/user-attachments/assets/630a3b35-b8de-4094-bfe8-0bdd4e8d4f8e)

> [!CAUTION]
> If you want to build project from sources on your PC, please, check **requirements.txt**

##

This was a bold attempt to create a full-fledged 3D engine on Python, but Python has its own perfomance limitations.


### It was implemented:
- Renderer
- VAO Instancing (`EntityCluster`)
- Simple shading model (point and spot light sources)
- Basic rigidbody
- AABB collider
- FPSController based on AABB collider

It has no physics on `demo_level` because it created of complex meshes

## Avecdes API

Demo level has been described in `src/levels/test_level.py` class.

You can create your own level following next steps

##

Create new file in levels directory using this pattern:

```python
from src.settings import *
from src.scene import Scene
from src.entity.entity import Entity
from src.texture import TextureManager
from src.mesh.utils import load_from_obj
from src.mesh.single_mesh import SingleMesh
from src.mesh.instanced_mesh import InstancedMesh
from src.entity.entity_cluster import EntityCluster

class MyLevel(Scene):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Init your objects
	def update(self, time, delta_time):
		# Update your objects
		super().update(time, delta_time)
```
##
> [!TIP]
> Initialization of objects on the scene includes several steps
> - Init vertex data
> - Init mesh object
> - Init texture object
> - Init entity object\objects related to this mesh
> 	- Init entity cluster if you want to draw multiple objects using same mesh in one **draw call**
> - Append entity or entity cluster to scene

##
### Creating of SingleEntity
#### Load from OBJ

Put in your obj model in `assets/obj` directory

Use following example code in `MyLevel.__init__`

```python
your_obj = load_from_obj('obj/your_obj')
your_obj_mesh = SingleMesh(
	ctx=self.ctx, program=self.shader.program,
	position = your_obj['position'],
	position_indices = your_obj['position_indices'],
	normal = your_obj['normal'],
	normal_indices = your_obj['normal_indices'],
	texcoord = your_obj['texcoord'],
	texcoord_indices = your_obj['texcoord_indices'],
	decrement=1,
	name='your_obj_mesh'
)
```

`decrement` field is needed to subtract some value while parsing mesh index data. *.obj default start index is 1, but my mesh parser uses 0 start index.
##
#### Loading texture

AvecdesEngine does not support the use of *.mtl files.

> [!TIP]
> One mesh - one texture

You can load the texture as follows

> [!WARNING]
> PNG file format only

```
TextureManager.load_texture
(
	context: mgl.Context,
	assets_path: str,
	has_alpha: bool,
	filter_type: int
)
```
Example for loading non-alpha texture with closest interpolation type
```python
your_texture = TextureManager.load_texture(self.ctx, 'textures/your_texture', False, mgl.NEAREST)
```

##

#### Add single entity to scene
```python
your_entity = Entity(
	mesh=your_obj_mesh,
	name='your_entity',
	texture=your_texture,
	collider='none',
)
self.append_object(your_entity)
```
##

### Creating of EntityCluster
> [!NOTE]
> `EntityCluster` is collection of multiple entities that will be drawn per one draw call.

Entities attached to `EntityCluster` uses `InstancedMesh` mesh type.

First of all create `InstancedMesh` instance the same way like `SingleMesh` type.
```python
your_model_obj = load_from_obj('obj/your_obj')
your_mesh =  InstancedMesh(
	ctx = self.ctx, program = self.shader.program,
	position = your_model_obj['position'],
	position_indices = your_model_obj['position_indices'],
	normal = your_model_obj['normal'],
	normal_indices = your_model_obj['normal_indices'],
	texcoord = your_model_obj['texcoord'],
	texcoord_indices = your_model_obj['texcoord_indices'],
	decrement=1,
	name='your_model_instanced'
)
```
Next, initialize cluster instance and objects.
```python
cluster = EntityCluster('your_cluster', your_ins_mesh, your_texture)
```

For example:
```python 
grid_w, grid_d, size = (10, 10, 4)
for i in range(grid_w * grid_d):
	x = (i % grid_w) * size
	y = (i // grid_d) * size
	your_entity = Entity(
		pos = (x, 0, y),
		name = 'your_entity_name',
		mesh = 'root',
		collider = 'aabb',
		use_physics = True,
		use_gravity = True,
		texture = 'root',
	)
	your_entity.collider = AABB(your_entity, 2.0, 1.0, 3.0)
	# Add object to cluster
	cluster.append_object(your_entity)
# After adding all objects cluster need to be processed
cluster.process()
# Add cluster to scene
self.append_object(cluster)
```
> [!NOTE]
> You can dynamically add objects to the cluster after the application has started.

> [!NOTE]
> The cluster updates only those objects that have changed (my attempt at optimization)

##

#### Add your scene to Engine class
Add your file to the imports section of the `src/engine.py` class.
```python
# other imports ...
from src.levels.my_level import MyLevel
```

Find the `init_scene` function in the `Engine` class and change the name of `TestLevel` to the name of your class.

```python
def init_scene(self):
	self.scene_light_shader = Shader(self.ctx, 'd_light')

	# Change below
	self.scene = MyLevel(self, self.scene_light_shader, 'test_level')

	self.player = Player(self.wnd, self.scene_light_shader)
```

##

#### You can use an FPS Controller

```python
self.player = FPSController(self, self.scene_light_shader)
self.scene.append_object(self.player)
```

Call `update_player` method in `update` method of engine class.

```python
if self.wnd.mouse_exclusivity:
	self.player.movement(self.delta_time)
# Change below
self.player.update_player()
```

## Technology stack:
- ModernGL (simple OpenGL API)
- Pillow Image
- Numpy
- OpenGL Math lib (GLM)

## What is next

Next, I would like to implement a wider functionality of the 3D engine but already on C++.

- GJK collision algo
- Level loader
- Enemy behaviour
- Instanced mesh based UI
