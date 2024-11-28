#version 430 core

in vec2 obj_uv;

out vec4 frag_color;

uniform sampler2D u_texture;

void main() {
	vec4 diffuse_color = texture(u_texture, obj_uv);
	frag_color = diffuse_color;
}