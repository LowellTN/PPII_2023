from flask import Flask, render_template, g, request, url_for, redirect, session
from pathlib import Path,os
import sqlite3

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./templates/static')
DATABASE = 'data/info.db'

# Localise les dossiers contenant  les pages et les styles pouur eviter les problèmes

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = '23343243'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def homepage() :
	return render_template("homepage.html")


@app.route("/map")
def map() :
	return render_template("map.html")


@app.route("/dons")
def dons():
	return render_template("dons.html")

@app.route("/<int:center_id>/comments")
def comments(center_id):
    """
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT u.username, c.date, c.type, c.content FROM comments as c, users as u WHERE c.center_id = (?) AND c.user_id = u.user_id;", (center_id,)) 
    res = c.fetchall()
    c.execute("SELECT name FROM centers WHERE id = (?)", (center_id,))
    center_name = c.fetchone()
	"""
    center_name = None
    res = None
    return render_template("display_comments.html", comments = res, center_name = center_name)

@app.route("/<int:center_id>/make_comment", methods = ["GET", "POST"])
def make_comment(center_id):
    if request.method == 'GET':
        #TODO - LOGGED IN CHECK
        #TODO - GET USERNAME FROM SESSION
        return ""
    elif request.method == 'POST':
        return ""
    else:
        return redirect(url_for('/'))

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        login = request.form["login"]
        password = request.form["password"]
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("insert into users (first_name, last_name, email, login, password) values (?,?,?,?,?)", (first_name, last_name, email, login, password))
        connection.commit()
        connection.close()
        return redirect('/registration_success') 
    else:
        return render_template('register.html')

@app.route("/registration_success")
def registration_success():
    return "Inscription réussie"

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form["login"]
        password = request.form["password"]
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("select id, login, password from users where login = ?", (login,))
        client = cursor.fetchone()
        if client is None:
            return "Login ou mot de passe incorrect"
        if client[2] == password:
            session['client_id'] = client[0]
            session['login'] = client[1]
            return redirect(url_for('profile'))
        else:
            return 'Login ou mot de passe incorrect'
    return render_template('login.html')

@app.route('/profile')
def profile():
    client_id = session.get('client_id')
    login = session.get('login')
    if client_id is not None and login is not None:
        return f'User ID: {client_id}, login: {login} '
    else:
        return 'User not logged in'



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
