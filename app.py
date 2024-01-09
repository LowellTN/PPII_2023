from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index() :
	return render_template(templates/<nom_de_la_page_html>)
