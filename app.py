from flask import Flask, render_template
from pathlib import Path,os

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./templates/static')

# Localise les dossiers contenant  les pages et les styles pouur eviter les problèmes

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


@app.route("/")
def homepage() :
	return render_template("homepage.html")


@app.route("/map")
def map() :
	return render_template("map.html")


@app.route("/dons")
def dons():
	return render_template("dons.html")



# Partie tri
# les éléments de la liste à trier sont des tuples (id, distance, - pertinence)
# les éléments sont triés du plus proche au plus loin ou du plus pertinent au moins pertinent


liste = []
filtre = ""
if filtre == "distance" :
	index = 1
elif filtre == "pertinence" :
	index = 2


def ordre(e1, e2) :
	"""renvoie True si les deux éléments sont placés (strictement) dans le bon ordre selon le critère"""
	return e1[index] < e2[index]


def tri(liste) :
	if len(liste) == 0 :
		return []
	pivot = liste[0]
	inf, eq, sup = [], [], []
	for e in liste :
		if ordre(e, pivot) :
			inf.append(e)
		elif ordre(pivot, e) :
			sup.append(e)
		else :
			eq.append(e)
	return tri(inf) + eq + tri(sup)


if __name__ == '__main__':
	app.run(debug=True)
