import os
import xml.etree.ElementTree as ET


def modify_svg(svg_file, output_file):
    # Vérifier si le répertoire de sortie existe, sinon le créer
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Charger le fichier SVG
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Namespace SVG
    namespace = {'svg': 'http://www.w3.org/2000/svg'}
    ET.register_namespace('', namespace['svg'])

    # Initialiser le compteur pour les nouveaux IDs
    id_counter = 1

    # Parcourir tous les éléments avec un attribut id
    for element in root.findall(".//*[@id]", namespace):
        # Récupérer l'ancien ID
        old_id = element.attrib['id']

        # Ajouter l'ancien ID en tant qu'attribut `title`
        element.set('title', old_id)

        # Vérifier si l'ID doit rester inchangé (par exemple, "banane")
        if old_id != "banane":
            # Remplacer l'ancien ID par un nouvel ID unique
            new_id = f"id_{id_counter}"
            element.set('id', new_id)

            # Incrémenter le compteur
            id_counter += 1

    # Sauvegarder les modifications dans un nouveau fichier
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Fichier modifié enregistré sous : {output_file}")


# Exemple d'utilisation
modify_svg("./images/svg_test.svg", "./svg_clean/output.svg")
