#version 430 core

in vec2 out_uv;

uniform sampler2D scene_view;
const float gamma = 2.2;

out vec4 frag_color;

void main() {
	vec3 inv_gamma = vec3(1 / gamma);
	vec2 new_uv = abs(vec2(1.0) - out_uv);
	vec4 scene_texture = texture(scene_view, new_uv);
	frag_color = vec4(pow(scene_texture.rgb, inv_gamma), scene_texture.a);
}
