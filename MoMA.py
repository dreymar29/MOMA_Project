from flask import Flask, render_template, redirect, url_for
from models import db, Art
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'moma.db')
app.config['SQLALCHEMY_DATABASE_CONNECTION'] = 'sqlite:///moma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    all_arts = Art.query.all()
    return render_template('index.html', arts=all_arts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/art')
def art():
    all_art = Art.query.all()
    return render_template('art.html', all_art=all_art)

@app.route('/artist')
def artist():
    return render_template('artist.html')

if __name__ == "__main__":
    app.run(debug=True)
    