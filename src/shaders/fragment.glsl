#version 330

// in from vertex shader
in vec3 theNormal;
in vec3 fragPos;
in vec2 TexCoords;

out vec4 outputColor;

uniform sampler2D imageTexture;
uniform vec3 lightPos;
uniform vec3 viewPos;

void main()
{
    // ambient component
    float ambInt = 0.7;
    vec3 ambColor = vec3(1.0, 1.0, 1.0);
    vec3 amb = ambInt * ambColor;

    // diffuse component
    vec3 diffColor = vec3(1.0, 1.0, 1.0);
    vec3 lightDir = normalize(lightPos - fragPos);
    vec3 norm = normalize(theNormal);
    float diffInt = max(dot(lightDir, norm), 0.0);
    vec3 diff = diffInt * diffColor;

    // specular component
    float specInt = 1.0;
    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float specPow = pow(max(dot(viewDir, reflectDir), 0.0), 256);
    vec3 spec = specInt * specPow * diffColor;
    
    vec3 fragColor = vec3(0.5, 0.7, 0.1);
    outputColor = vec4((spec + diff + amb) * fragColor, 1.0);

    vec4 texColor = texture(imageTexture, TexCoords); // Sample the texture
    outputColor = vec4((spec + diff + amb) * texColor.rgb, texColor.a); // Use texture color
}