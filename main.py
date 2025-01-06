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

    # Fonction pour regrouper les pixels adjacents en zones
    def find_contiguous_regions(image, target_color):
        visited = set()
        regions = []

        for y in range(height):
            for x in range(width):
                if (x, y) not in visited and image.getpixel((x, y)) == target_color:
                    stack = [(x, y)]
                    region = []

                    while stack:
                        cx, cy = stack.pop()
                        if (cx, cy) not in visited and image.getpixel((cx, cy)) == target_color:
                            visited.add((cx, cy))
                            region.append((cx, cy))

                            # Ajouter les pixels voisins
                            if cx > 0: stack.append((cx - 1, cy))
                            if cx < width - 1: stack.append((cx + 1, cy))
                            if cy > 0: stack.append((cx, cy - 1))
                            if cy < height - 1: stack.append((cx, cy + 1))

                    regions.append(region)

        return regions

    # Fonction pour convertir une région en un chemin SVG (path)
    def region_to_path(region):
        path_data = []
        for x, y in region:
            path_data.append(f"M{x} {y}h1v1h-1z")
        return " ".join(path_data)

    # Parcourir les parties du corps
    for part, color in body_parts.items():
        svg_content += f'  <g id="{part}" fill="rgb{color}">\n'

        # Trouver les régions contiguës pour la couleur cible
        regions = find_contiguous_regions(img, color)

        # Ajouter les régions au SVG sous forme de chemins
        for region in regions:
            path_data = region_to_path(region)
            svg_content += f'    <path d="{path_data}" />\n'

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
