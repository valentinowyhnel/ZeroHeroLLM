#!/bin/bash

# Boucle à travers tous les sous-répertoires dans le dossier labs
for lab_dir in labs/llm*; do
  # Vérifier si c'est bien un répertoire
  if [ -d "$lab_dir" ]; then
    # Extraire le nom de l'image du chemin du répertoire
    image_name=$(basename "$lab_dir")
    echo "Construction de l'image Docker pour $image_name..."
    # Exécuter la commande docker build
    docker build -t "$image_name" "$lab_dir"
  fi
done

echo "Toutes les images Docker des laboratoires ont été construites."
