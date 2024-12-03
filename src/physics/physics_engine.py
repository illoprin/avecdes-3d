from src.settings import *
from enum import IntEnum
from sys import float_info

class ColliderType(IntEnum):
	NoCollider = 0
	AABB = 1
	Mesh = 2

class CollisionTag(IntEnum):
	Static = 0
	Dynamic = 1
	Trigger = 3

class Collider():
	tag = ColliderType.NoCollider


def aabb_test_axis (axis, min_a, max_a, min_b, max_b, mtv_axis, mtv_len):
	# Separating Axis Theorem
    # =======================
    # - Two convex shapes only overlap if they overlap on all axes of separation
    # - In order to create accurate responses we need to find the collision vector (Minimum Translation Vector)   
    # - The collision vector is made from a vector and a scalar, 
    #   - The vector value is the axis associated with the smallest penetration
    #   - The scalar value is the smallest penetration value
    # - Find if the two boxes intersect along a single axis
    # - Compute the intersection interval for that axis
    # - Keep the smallest intersection/penetration value
	axis = glm.vec3(axis)
	axis_length_squared = glm.dot(axis, axis)
	# If axis degenerate -> then ignore
	# if axis_length_squared < 1.0e-8:
		# return True
	
	# Calculate overlapping
	d0 = max_b - min_a
	d1 = max_a - min_b

	if d0 <= 0 or d1 <= 0:
		return False
	
	overlap = d0 if (d0 < d1) else -d1

	# MTD - minimum translation distance
	sep = axis * (overlap / axis_length_squared)

	len = glm.dot(sep, sep)

	# If MTV is smaller than computed MTD vector -> update MTV vector
	# if (len < mtv_len):
	return [sep, len]


def has_intersection_aabb_aabb (entity_a, entity_b):
	# Get first AABB min and max points
	a_max_x, a_max_y, a_max_z = entity_a.collider.max
	a_min_x, a_min_y, a_min_z = entity_a.collider.min
	# Get second AABB min and max points
	b_max_x, b_max_y, b_max_z = entity_b.collider.max
	b_min_x, b_min_y, b_min_z = entity_b.collider.min

	# Init MTV (Minimum Translation Vector)
	# MTV axis - axis of minimum depth of intersection
	mtv_axis = glm.vec3()
	# MTV mag - the length of that intersection
	mtv_len = float_info.max

	# Idea: check all axis on mix/max intersection and find the minimum one
	# then shift one of objects belong that axis

	# Check separate axis
	x_check = aabb_test_axis((1, 0, 0), a_min_x, a_max_x, b_min_x, b_max_x, mtv_axis, mtv_len)
	if x_check:
		if x_check[1] < mtv_len:
			mtv_axis = x_check[0]
			mtv_len = x_check[1]
	else:
		return False
	y_check = aabb_test_axis((0, 1, 0), a_min_y, a_max_y, b_min_y, b_max_y, mtv_axis, mtv_len)
	if y_check:
		if y_check[1] < mtv_len:
			mtv_axis = y_check[0]
			mtv_len = y_check[1]
	else:
		return False
	z_check = aabb_test_axis((0, 0, 1), a_min_z, a_max_z, b_min_z, b_max_z, mtv_axis, mtv_len)
	if z_check:
		if z_check[1] < mtv_len:
			mtv_axis = z_check[0]
			mtv_len = z_check[1]
	else:
		return False

	overlap = mtv_len * glm.normalize(mtv_axis)

	return Collision (overlap, entity_a, entity_b)

class Collision():
	def __init__ (self, overlap: glm.vec3, active, target):
		self.active = active
		self.target = target
		self.overlap = overlap

	@property
	def responce(self):
		responce = {
			'active': glm.vec3(),
			'target': glm.vec3()
		}
		active_tag, target_tag = self.active.rigidbody.tag, self.target.rigidbody.tag
		if active_tag == CollisionTag.Dynamic and target_tag == CollisionTag.Static:
			responce['active'] = self.overlap	
		elif active_tag == CollisionTag.Static and target_tag == CollisionTag.Dynamic:
			responce['target'] = self.overlap
		elif active_tag == CollisionTag.Dynamic and active_tag == CollisionTag.Dynamic:
			half_overlap = self.overlap / 2
			responce['active'] = half_overlap
			responce['target'] = -half_overlap
		return responce
	
def gravity_collinear(vec: glm.vec3):
	return glm.dot(glm.normalize(-vec), glm.normalize(PHYS_GRAVITY)) > 0.9