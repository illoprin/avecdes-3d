#version 430 core

out vec4 frag_color;

in vec3 obj_normal;
in vec2 obj_uv;
in vec3 obj_frag_position;
in vec3 out_normal;

uniform sampler2D u_texture;

uniform vec3 u_camera_dir;

uniform vec3 u_ambient_light = vec3(1.0);

void main() {
	// Ambient light
	float theta = dot(-u_camera_dir, out_normal) * .5;
	float al_modifer = min(.5 + theta, 1.0);
	vec3 al = u_ambient_light * al_modifer;
	

	vec3 diffuse_color = texture(u_texture, obj_uv).rgb * al;
	frag_color = vec4(diffuse_color, 1.0);
}