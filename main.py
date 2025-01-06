from PIL import Image

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

    # Fonction pour regrouper les pixels contigus en rectangles
    def find_contiguous_rectangles(image, target_color):
        visited = set()
        rectangles = []

        for y in range(height):
            x_start = None
            for x in range(width):
                if image.getpixel((x, y)) == target_color and (x, y) not in visited:
                    if x_start is None:
                        x_start = x
                    visited.add((x, y))

                if (image.getpixel((x, y)) != target_color or x == width - 1) and x_start is not None:
                    x_end = x if image.getpixel((x, y)) != target_color else x + 1
                    rectangles.append((x_start, y, x_end - x_start, 1))  # Rectangle (x, y, width, height)
                    x_start = None

        return rectangles

    # Parcourir les parties du corps
    for part, color in body_parts.items():
        svg_content += f'  <g id="{part}" fill="rgb{color}">\n'

        # Trouver les rectangles contigus pour la couleur cible
        rectangles = find_contiguous_rectangles(img, color)

        # Ajouter les rectangles au SVG
        for rect in rectangles:
            x, y, w, h = rect
            svg_content += f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="rgb{color}" />\n'

        svg_content += '  </g>\n'

    svg_content += '</svg>'

    # Sauvegarder le fichier SVG
    with open(output_path, 'w') as f:
        f.write(svg_content)

    print(f"SVG sauvegardé à {output_path}")


# Chemin de l'image et du fichier SVG de sortie
image_path = './images/test.png'
output_path = './svg_output/test_optimized.svg'

# Appeler la fonction
image_to_svg_with_parts(image_path, output_path)
