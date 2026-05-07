from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import db, Art, Visitor, Staff, InteractionLog
import os

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_moma'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'moma.db')
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')

        if role == 'staff':
            user = Staff.query.filter_by(username=username, password=password).first()
        else:
            user = Visitor.query.filter_by(name=username, password=password).first()

        if user:
            session['user_id'] = user.id
            session['user_name'] = username
            session['role'] = role
            return redirect(url_for('index'))
        else:
            flash('Login gagal! Cek username dan password.')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        pwd = request.form.get('password')

        new_v = Visitor(name=name, gender=gender, password=pwd)
        db.session.add(new_v)
        db.session.commit()
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/all-reviews')
def all_reviews():
    koleksi_art = Art.query.all()
    page_review = InteractionLog.query.filter(
        (InteractionLog.review_art != None) | (InteractionLog.review_museum != None)
    ).all()
    return render_template('review.html', all_art=koleksi_art, reviews=page_review)

@app.route('/add-review/<art_id>', methods=['POST'])
def add_review(art_id):
    review_art = request.form.get('review_art')
    visitor_id = session.get('visitor_id')

    if review_art and visitor_id:
        new_log = InteractionLog(
            visitor_id=visitor_id,
            art_id=art_id,
            review_art=review_art,
        )
        db.session.add(new_log)
        db.session.commit()
    
    return redirect(url_for('all_reviews'))

@app.route('/add-museum-review', methods=['POST'])
def add_museum_review():
    review_museum = request.form.get('review_museum')
    visitor_museum = session.get('visitor_id')
    rating = request.form.get('rating')

    if review_museum:
        new_log = InteractionLog(
            visitor_id=visitor_museum,
            art_id=None, 
            review_museum=review_museum,
            rating=int(rating)
        )
        db.session.add(new_log)
        db.session.commit()

    return redirect(url_for('all_reviews'))

if __name__ == "__main__":
    app.run(debug=True)
    