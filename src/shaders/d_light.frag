#version 430 core

#define MAX_POINT_LIGHTS 64
#define MAX_SPOT_LIGHTS 32

struct PointLight {
	vec3 position;
	vec3 color;
	float radius;
	float intensity;
	float specular;
};

struct SpotLight {
	vec3 position;
	vec3 direction;
	vec3 color;
	float intensity;
	float distance;
	float outer_cut_off;
	float cutoff;
};

struct SunLight {
	vec3 direction;
	vec3 color;
	float intensity;
};

in vec3 out_normal;

in vec2 obj_uv;
in vec3 obj_normal;
in vec3 obj_frag_position;

// Light uniforms
uniform vec3 u_ambient_light = vec3(0.1, 0.1, 0.1);
uniform PointLight point_light[MAX_POINT_LIGHTS];
uniform SpotLight spot_light[MAX_SPOT_LIGHTS];
uniform SunLight sun_light;
uniform bool uses_sun_light = false;
uniform vec3 u_camera_position;

float getLightAttenuation(float d, float r) {
	float constant = 1.0;
	float linear = 4.5 / r;
	float quadratic = 75.0 / pow(r, 2);
	return (1 / (constant + linear * d + quadratic * pow(d, 2)));
}

// Calculate light intensity for pixel
// More complicated algo compared to SimplexEngine
vec3 getPointLight(PointLight light) {
	// Calculate all nessesary vectors
	vec3 light_frag_vec = (light.position - obj_frag_position);
	vec3 light_direction = normalize(light_frag_vec);
	vec3 view_dir = normalize(u_camera_position - obj_frag_position);
	vec3 reflect_dir = reflect(-light_direction, obj_normal);
	
	// Calculate diffuse color
	float diffuse = max(dot(light_direction, obj_normal), 0.0);
	vec3 light_color = light.color * diffuse * light.intensity;

	// Calculate specular based on reflection
	float specular_ratio = pow(max(dot(view_dir, normalize(reflect_dir)), 0.0), 64);
	vec3 specular = light.specular * specular_ratio * light.color;
	// Calculate point light falloff (attenuation)
	float d = length(light_frag_vec);
	float attenuation = getLightAttenuation(d, light.radius);
	// Return result color
	return (light_color + specular) * attenuation;
}

vec3 getSpotLight (SpotLight light) {
	// Calculate all nessesary vectors
	vec3 light_dir = -normalize(light.direction);
	vec3 light_frag_vec = (light.position - obj_frag_position);
	vec3 frag_dir = normalize(light_frag_vec);

	// Calculate angle of fragment direction relative to light direction
	float theta = dot(frag_dir, light_dir);
	// Calculate spot light cone cutoff
	float epsilon = (light.cutoff - light.outer_cut_off);
	float ratio = clamp((theta - light.outer_cut_off) / epsilon, 0.0, 1.0);
	// Calculate spot light falloff (attenuation)
	float d = length(light_frag_vec);
	float attenuation = getLightAttenuation(d, light.distance);
	// Return result color
	return attenuation * light.color * light.intensity * ratio;
}

// Textures
uniform sampler2D u_diffuse_texture;

// Gamma
const float gamma = 2.2;
const float inv_gamma = 1 / gamma;

out vec4 frag_color;

void main() {
	vec4 diffuse_color = texture(u_diffuse_texture, obj_uv);
	// Enter gamma to changing mode
	diffuse_color.rgb = pow(diffuse_color.rgb, vec3(gamma));

	// Ambient light
	float theta = dot(normalize(u_camera_position - obj_frag_position), out_normal) * .5;
	float al_modifer = min(.5 + theta, 1.0);

	// Summorize all lighting
	vec3 lighting = (u_ambient_light * al_modifer);
	for(uint i = 0; i < point_light.length(); i++) {
		lighting += getPointLight(point_light[i]);
	}
	for(uint i = 0; i < spot_light.length(); i++) {
		lighting += getSpotLight(spot_light[i]);
	}
	if (uses_sun_light) {
		// TODO: realize sun light and shadow calculation
	}
	diffuse_color.rgb *= lighting;
	
	// Return to standart gamma
	diffuse_color.rgb = pow(diffuse_color.rgb, vec3(inv_gamma));

	frag_color = diffuse_color;
}