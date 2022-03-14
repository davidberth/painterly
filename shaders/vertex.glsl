#version 430
in vec2 in_vert;
in vec3 in_color;
out vec3 color;
void main() {
    gl_Position = vec4(in_vert * 2.0 - 1.0, 0.0, 1.0);
    color = in_color;
}