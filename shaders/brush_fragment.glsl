#version 430

in vec4 color;
in vec2 v_text;
in vec2 v_stroke;

out vec4 fragColor;

in vec2 position;

#define MAX_TOTAL_LIGHTS 100
uniform sampler2D Texture;
uniform float noise_color_scale;
uniform float length_distance_scale;
uniform float side_distance_scale;
uniform float num_lights;
uniform vec2  light_positions[MAX_TOTAL_LIGHTS];
uniform vec3  light_intensities[MAX_TOTAL_LIGHTS];
uniform float light_radii[MAX_TOTAL_LIGHTS];

void main() {
    float noise = texture(Texture, v_text, 0).x * noise_color_scale - noise_color_scale / 2.0;
    float edge_check = texture(Texture, vec2(v_text.x + 0.5, v_text.y * 4.0), 0).x;

    float length_distance = min(1.0 - v_stroke.y, v_stroke.y) * length_distance_scale;
    float side_distance = min(1.0 - v_stroke.x, v_stroke.x) * side_distance_scale;

    float edge_distance = min(length_distance, side_distance);

    vec4 out_color = color + vec4(noise, noise, noise, 0.0);
    // TODO include an ambient light at some point

    // include the lights
    vec3 light_multiplier = vec3(0.5, 0.5, 0.5);
    for (int i=0; i<num_lights; ++i)
    {
        float dis = length(position - light_positions[i]);
        if (dis < light_radii[i])
        {
            light_multiplier += vec3((light_radii[i] - dis) * 5.0) * light_intensities[i];
        }

    }

    if (edge_distance > edge_check)
    fragColor = out_color * vec4(light_multiplier, 1.0);
    else
    discard;
}
