#version 430

in vec4 color;
in vec2 v_text;
in vec2 v_stroke;

out vec4 fragColor;

uniform sampler2D Texture;
uniform float noise_color_scale;
uniform float length_distance_scale;
uniform float side_distance_scale;

void main() {
    float noise = texture(Texture, v_text, 0).x * noise_color_scale - noise_color_scale / 2.0;
    float edge_check = texture(Texture, vec2(v_text.x + 0.5, v_text.y * 4.0), 0).x;

    float length_distance = min(1.0 - v_stroke.y, v_stroke.y) * length_distance_scale;
    float side_distance = min(1.0 - v_stroke.x, v_stroke.x) * side_distance_scale;

    float edge_distance = min(length_distance, side_distance);
    if (edge_distance > edge_check)
    fragColor = color + vec4(noise, noise, noise, 0.0);
    else
    discard;
}
