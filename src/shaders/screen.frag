#version 430 core

in vec2 out_uv;

uniform sampler2D scene_view;

out vec4 frag_color;

uniform int u_width;
uniform int u_height;

vec3 useKernel(sampler2D tex, vec2 uv, float[9] kernel) {
	vec3 pixel;
	float offset_x = 1.0 / float(u_width);
	float offset_y = 1.0 / float(u_height);
	
	vec2 offsets[9] = vec2[](
        vec2(-offset_x,  offset_y), // top-left
        vec2( 0.0,    offset_y), // top-center
        vec2( offset_x,  offset_y), // top-right
        vec2(-offset_x,  0.0),   // center-left
        vec2( 0.0,    0.0),   // center-center
        vec2( offset_x,  0.0),   // center-right
        vec2(-offset_x, -offset_y), // bottom-left
        vec2( 0.0,   -offset_y), // bottom-center
        vec2( offset_x, -offset_y)  // bottom-right    
    );
	
	vec3 samples[9];
	for (uint i = 0; i < 9; i++) {
		samples[i] = vec3(texture(tex, uv.st + offsets[i]));
	}
	pixel = vec3(0.0);
	for(int i = 0; i < 9; i++)
		pixel += samples[i] * kernel[i];

	return pixel;
}

// Post process uniforms
uniform float u_contrast = 1.02;
uniform float u_brightness = 1;

void main() {
	// Calculate flipped uv
	vec2 new_uv = abs(vec2(1.0) - out_uv);

	// Use blur kernel
	float blur[9] = float[](
		1.0 / 16, 2.0 / 16, 1.0 / 16,
    	2.0 / 16, 4.0 / 16, 2.0 / 16,
    	1.0 / 16, 2.0 / 16, 1.0 / 16 
	);
	vec3 scene = texture(scene_view, new_uv).rgb;

	// Apply contrast
	scene.rgb = ((scene.rgb - .5) * max(u_contrast, 0.0)) + .5;
	// Apply brightness
	scene.rgb *= u_brightness;
	
	frag_color = vec4(scene, 1.0);
}
