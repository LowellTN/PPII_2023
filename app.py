from flask import Flask, render_template, g, request, url_for, redirect, session, jsonify
from pathlib import Path,os
import sqlite3
import datetime

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./templates/static')
DATABASE = 'data/info.db'

# Localise les dossiers contenant  les pages et les styles pouur eviter les problèmes

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = '23343243'
comments_list = [
    ["User1", "2022-01-14", "110", "This is a comment about the waste sorting center."],
    ["User2", "2022-01-15", "010", "Another user's comment about the waste sorting center."],
]

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
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT u.last_name, u.first_name, c.date, c.waste_type, c.comment FROM comments as c, users as u WHERE c.id = (?) AND c.id_client = u.id;", (center_id,)) 
    comments_list = c.fetchall()
    c.execute("SELECT name FROM centers WHERE id = (?)", (center_id,))
    center_name = c.fetchone()
    return render_template("comments.html", comments = comments_list, center_name = center_name)

@app.route("/<int:center_id>/add_comment", methods = ["POST"])
def add_comment(center_id):
    #TODO - LOGGED IN CHECK
    #TODO - GET USERNAME FROM SESSION
    user_id = None
    code = ''.join(request.form.getlist('wasteType'))
    waste_types = get_waste_types(code)
    comment_text = request.form['commentText']
    if not waste_types:
          return "Merci de sélectionner au moins un type de déchets", 400
    date = get_current_date()
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO comments (user_id, type, content, date) VALUES (?,?,?,?);", (user_id, waste_types, comment_text, date))
    #TODO ADD SUR LE USER
    return redirect(url_for("/{center_id}/comments".format(center_id = center_id)))

def get_current_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")

def get_waste_types(code):
    types = ["Ordures ménagères résiduelles", "Emballages recyclables", "Verre", "Encombrants", "Déchets verts", "Déchets d'Equipement Electriques et Electroniques (DEEE)", "Déchets dangereux ou non issus des activités de ménage (produits d'entretien), bricolage, jardinage des particuliers"]
    res = [types[i] for i in range(len(code)) if code[i]]
    return ", ".join(res) + '.'
      

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
        cursor.execute("insert into users (first_name, last_name, email, login, password, visits) values (?,?,?,?,?,?)", (first_name, last_name, email, login, password, 0))
        connection.commit()
        connection.close()
        return redirect('/registration_success') 
    else:
        return render_template('register.html')

@app.route("/registration_success")
def registration_success():
    return "Inscription réussie"

def user_info(user_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("select * from users where id = ?", (user_id,))
    user_info = cursor.fetchone()
    # connection.close()
    return user_info

def get_comments(user_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("select comment from comments where id_client = ?", (user_id,))
    comments = cursor.fetchall()
    # connection.close()
    # print(f"{comments}")
    return comments

def favorite(user_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("select name from centers join fav on fav.id_center = centers.id where id_client = ?", (user_id,))
    favorites = cursor.fetchall()
    return favorites

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form["login"]
        password = request.form["password"]
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("select id, login, password, visits from users where login = ?", (login,))
        client = cursor.fetchone()
        if client is None:
            return "Login ou mot de passe incorrect"
        if client[2] == password:
            session['client_id'] = client[0]
            session['login'] = client[1]
            new_visits = client[3] + 1
            cursor.execute("update users set visits = ? where id = ?", (new_visits, client[0]))
            connection.commit()
            return redirect(url_for('profile'))
        else:
            return 'Login ou mot de passe incorrect'
    return render_template('login.html')

@app.route('/profile')
def profile():
    client_id = session.get('client_id')
    login = session.get('login')
    if client_id is not None and login is not None:
        client_info = user_info(client_id)
        comments = get_comments(client_id)
        favorites = favorite(client_id)
        # print(f"{comments}")
        # fav_d = favorite(client_id)
        client_id, first_name, last_name, email, login, password, visits = client_info 
        return render_template('profile.html', client_id=client_id, first_name=first_name, last_name=last_name, email=email, login=login, comments=comments, favorites=favorites, visits=visits)
    else:
        return 'User not logged in'

''' Décommenter cette fonction pour générer à nouveau les noms des centres dans la table centers de la base de données
@app.route('/update_db', methods=['POST'])
def update_database_with_centers():
    if request.method == 'POST':
        centers_names = request.json.get('centersNames', [])
        connection = get_db()
        cursor = connection.cursor()
        for name in centers_names:
            cursor.execute('INSERT INTO centers (name, nb_fav, nb_click) VALUES (?, 0, 0);', (name,))
        connection.commit()
        connection.close()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})
'''

# Partie tri
# les éléments de la liste à trier sont des tuples (id, distance, - pertinence)
# les éléments sont triés du plus proche au plus loin ou du plus pertinent au moins pertinent


liste = []
filtre = "distance"
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