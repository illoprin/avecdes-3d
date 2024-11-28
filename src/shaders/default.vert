#version 430 core

in vec3 in_position;
in vec2 in_texcoord_0;
in vec3 in_normal;

uniform mat4 m_view;
uniform mat4 m_projection;
uniform mat4 m_model = mat4(1.0);

out vec3 out_normal;
out vec3 obj_normal;
out vec2 obj_uv;
out vec3 obj_frag_position;

void main() {
	obj_normal = mat3(transpose(inverse(m_model))) * in_normal;
	obj_frag_position = vec3((m_model * vec4(in_position, 1.0)).xyz);
	out_normal = in_normal;

	obj_uv = in_texcoord_0;
	gl_Position = m_projection * m_view * m_model * vec4(in_position, 1.0);
}