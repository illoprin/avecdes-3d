from src.entity.entity import Entity
from src.settings import *
from enum import IntEnum

def has_intersection_aabb_aabb (entity_a: Entity, entity_b: Entity):
	a_pos_x, a_pos_y, a_pos_z = entity_a.position.to_list()
	b_pos_x, b_pos_y, b_pos_z = entity_b.position.to_list()
	a_scl_x, a_scl_y, a_scl_z = entity_a.scale.to_list()
	b_scl_x, b_scl_y, b_scl_z = entity_b.scale.to_list()
	x_left = a_pos_x - a_scl_x / 2 < b_pos_x + b_scl_x / 2
	x_right = a_pos_x + a_scl_x / 2 > b_pos_x - b_scl_x / 2
	y_up = a_pos_y + a_scl_y / 2 > b_pos_y - b_scl_y / 2
	y_down = a_pos_y - a_scl_y / 2 < b_pos_y + b_scl_y / 2
	z_forward = a_pos_z + a_scl_z / 2 > b_pos_z + b_scl_z / 2
	z_backward = a_pos_z - a_scl_z / 2 < b_pos_z - b_scl_z / 2
	if x_left and x_right and y_up and y_down and z_forward and z_backward:
		return True
	return False

def resolve_collision_aabb_aabb(obj_a: Entity, obj_b: Entity):
	if obj_a.rigidbody != None and obj_b.rigidbody == None:
		obj_a.rigidbody.zero_velocity()
		return
	
	if obj_b.rigidbody != None and obj_a.rigidbody == None:
		obj_b.rigidbody.zero_velocity()
	
	if obj_b.rigidbody != None and obj_a.rigidbody != None:
		print ('Collision Resolver - I dont know how to resolve that')
		obj_a.rigidbody.zero_velocity()
		obj_b.rigidbody.zero_velocity()
	

class ColliderType(IntEnum):
	NoCollider = 0
	AABB = 1
	Mesh = 2

class Collider():
	tag = ColliderType.NoCollider

class Collision():
	def __init__ (self, obj_a: Entity, obj_b: Entity):
		self.obj_a = obj_a
		self.obj_b = obj_b

