#version 430

in vec2 in_vert;
in vec4 in_color;
in vec2 in_tex_coord;
in vec2 in_stroke_coord;

out vec4 color;
out vec2 v_text;
out vec2 v_stroke;

void main() {
    gl_Position = vec4(in_vert * 2.0 - 1.0, 0.0, 1.0);
    color = in_color;
    v_text = in_tex_coord;
    v_stroke = in_stroke_coord;
}