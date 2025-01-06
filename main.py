from PIL import Image
from pathlib import Path

# Fonction pour convertir une image en SVG avec des parties du corps découpées
def image_to_svg_with_parts(image_path, output_path):
    # Charger l'image
    img = Image.open(image_path)

    # Convertir en mode RGB si nécessaire
    if img.mode != 'RGB':
        img = img.convert('RGB')

    width, height = img.size

    # Définir les couleurs des parties du corps et leurs IDs
    body_parts = {
        "head": (237, 28, 36),  # Rouge
        "torso": (255, 242, 0),  # Jaune
        "left_arm": (34, 177, 76),  # Vert
        "right_arm": (0, 162, 232),  # Bleu clair
        "left_leg": (163, 73, 164),  # Violet
        "right_leg": (153, 217, 234),  # Cyan pâle
    }

    # Initialiser le contenu SVG
    svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n'

    # Parcourir les parties du corps
    for part, color in body_parts.items():
        svg_content += f'  <g id="{part}" fill="rgb{color}">\n'

        # Parcourir les pixels pour trouver ceux correspondant à cette couleur
        for y in range(height):
            for x in range(width):
                if img.getpixel((x, y)) == color:
                    svg_content += f'    <rect x="{x}" y="{y}" width="1" height="1" />\n'

        svg_content += '  </g>\n'

    svg_content += '</svg>'

    # Sauvegarder le fichier SVG
    with open(output_path, 'w') as f:
        f.write(svg_content)

    print(f"SVG sauvegardé à {output_path}")

# Chemin de l'image et du fichier SVG de sortie
image_path = './images/test.png'
output_path = './svg_output/test.svg'

# Appeler la fonction
image_to_svg_with_parts(image_path, output_path)
