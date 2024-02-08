#version 330 core

// in from opengl application
layout (location=0) in vec3 vertexPos;
layout (location=1) in vec2 vertexTexCoord;
layout (location=2) in vec3 normal;

uniform mat4 model;
uniform mat4 projection;

// out to fragment shader
out vec2 TexCoords; 
out vec3 fragPos;
out vec3 theNormal;

void main() {
    gl_Position = projection * model * vec4(vertexPos, 1.0);
    fragPos = vec3(model * vec4(vertexPos, 1.0));
    theNormal = transpose(inverse(mat3(model))) * normal;
    TexCoords = vertexTexCoord; 
}
