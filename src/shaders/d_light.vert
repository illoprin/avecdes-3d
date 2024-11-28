#version 430 core

in vec3 in_position;
in vec2 in_texcoord_0;
in vec3 in_normal;

out vec2 obj_uv;

uniform mat4x4 m_view;
uniform mat4x4 m_projection;
uniform mat4x4 m_model;

void main() {
	obj_uv = in_texcoord_0;
	gl_Position = m_projection * m_view * m_model * vec4(in_position, 1.0);
}