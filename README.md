# PPII 2023 Enactus

### Pour le développement de l'application web :

Mettre en place l'environnement virtuel python (à faire à la racine du répertoire git) :

	$ python3 -m venv nom_env

Cacher l'environnement virtuel de git :

	$ echo 'nom_env' >> .gitignore

Activer l'environnement virtuel :

	$ source nom_env/bin/activate

Télécharger l'ensemble des bibliothèques nécessaires : 

	$ pip install -r requirements.txt

Si vous avez besoin d'ajouter une bibliothèque pour le projet, n'oubliez pas de faire la commande :

	$ pip freeze > requirements.txt

### Pour tester l'application web : 

Activer l'environnement virtuel


Executer la commande : 

	$ flask run
