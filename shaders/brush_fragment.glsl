#version 430

in vec4 color;
in vec2 v_text;
in vec2 v_stroke;

out vec4 fragColor;

in vec2 position;

uniform sampler2D noise_texture;
uniform sampler2D lights_texture;

uniform float noise_color_scale;
uniform float length_distance_scale;
uniform float side_distance_scale;
uniform float num_lights;


void main() {
    float noise = texture(noise_texture, v_text, 0).x * noise_color_scale - noise_color_scale / 2.0;
    float edge_check = texture(noise_texture, vec2(v_text.x + 0.5, v_text.y * 4.0), 0).x;

    float length_distance = min(1.0 - v_stroke.y, v_stroke.y) * length_distance_scale;
    float side_distance = min(1.0 - v_stroke.x, v_stroke.x) * side_distance_scale;

    float edge_distance = min(length_distance, side_distance);

    vec4 out_color = color + vec4(noise, noise, noise, 0.0);
    // TODO include an ambient light at some point

    // include the lights
    vec3 light_multiplier = vec3(1.0, 1.0, 1.0);
    for (int i=0; i<num_lights; ++i)
    {

        vec2 light_position = texelFetch(lights_texture, ivec2(i, 0), 0).xy;
        vec3 light_color = texelFetch(lights_texture, ivec2(i, 1), 0).xyz;
        float light_radius = texelFetch(lights_texture, ivec2(i, 2), 0).x;
        float distance = length(position - light_position);
        if (distance < light_radius)
        {
            light_multiplier = vec3(3.0, 3.0, 3.0);
            //light_multiplier += vec3((light_radius - distance) * 5.0) * light_color[i];
        }

    }

    if (edge_distance > edge_check)
    fragColor = out_color * vec4(light_multiplier, 1.0);
    else
    discard;
}
