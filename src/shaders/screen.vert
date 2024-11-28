#version 430 core

in vec3 in_position;
in vec2 in_texcoord_0;

out vec2 out_uv;

void main() {
	gl_Position = vec4(in_position.xy * 2.0, 0.0, 1.0);
	out_uv = in_texcoord_0;
}