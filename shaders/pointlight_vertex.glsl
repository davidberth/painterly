#version 430

in vec2 in_vert;
in vec4 in_color;
in vec2 in_tex_coord;

out vec4 color;
out vec2 v_text;

void main() {

    color = in_color;
    v_text = in_tex_coord;
    gl_Position = vec4(in_vert * 2.0 - 1.0, 0.001, 1.0);
}
