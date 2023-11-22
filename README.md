# PPII_2023
Projet PPII Enactus 


Mettre en place l'environnement virtuel python (à faire à la racine du répertoire git) :

	python3 -m venv nom_env

Cacher l'environnement virtuel de git :

	echo 'nom_env' >> .gitignore

Activer l'environnement virtuel :

	source nom_env/bin/activate

Télécharger l'ensemble des bibliothèques nécessaires : 

	pip install -r requirements.txt

Si vous avez besoin d'ajouter une biliothèque pour le projet, n'oubliez pas de faire la commande :

	pip freeze > requirements.txt
