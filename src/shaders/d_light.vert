#version 430 core

in vec3 in_position;
in vec2 in_texcoord_0;
in vec3 in_normal;
in mat4 in_model;

uniform mat4x4 m_view;
uniform mat4x4 m_projection;

out vec3 out_normal;
out vec3 obj_normal;
out vec2 obj_uv;
out vec3 obj_frag_position;

void main() {
	obj_normal = mat3(transpose(inverse(in_model))) * in_normal;
	obj_frag_position = vec3((in_model * vec4(in_position, 1.0)));
	out_normal = normalize(in_normal);

	obj_uv = in_texcoord_0;
	gl_Position = m_projection * m_view * in_model * vec4(in_position, 1.0);
}