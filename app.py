from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def homepage() :
	return render_template("homepage.html")


@app.route("/map")
def map() :
	return render_template("map.html")


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


print(tri(liste))
