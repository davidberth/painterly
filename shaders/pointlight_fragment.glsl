#version 430

in vec4 color;
out vec4 fragColor;
in vec2 v_text;


void main() {
    // compute the distance from the center based don the v_text coordinates
    float dis = length(v_text);
    float impact = 1.0 - min(dis, 1.0);
    fragColor = vec4(color.x, color.y, color.z, color.w * impact);
}
