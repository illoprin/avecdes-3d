#version 430 core

in vec2 out_uv;

uniform sampler2D scene_view;

out vec4 frag_color;

// Post process uniforms
uniform float u_contrast = 1.02;
uniform float u_brightness = 1;

void main() {
	vec2 new_uv = abs(vec2(1.0) - out_uv);
	vec4 scene_texture = texture(scene_view, new_uv);

	// Apply contrast
	scene_texture.rgb = ((scene_texture.rgb - .5) * max(u_contrast, 0.0)) + .5;
	// Apply brightness
	scene_texture.rgb *= u_brightness;
	
	frag_color = scene_texture;
}
