from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import db, Art, Artist, Visitor, Staff, InteractionLog
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
    return render_template('index.html', all_arts=Art.query.all())

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/art')
def art():
    all_art = Art.query.all()
    return render_template('art.html', all_art=all_art)

@app.route('/art/<int:art_id>')
def art_detail(art_id):
    selected_art = Art.query.get_or_404(art_id)
    art_reviews = InteractionLog.query.filter_by(art_id=art_id).filter(InteractionLog.review_art != None).all()
    return render_template('art_detail.html', art=selected_art, reviews=art_reviews)

@app.route('/artist')
def featured_artist(): 
    all_artist = Artist.query.all() 
    return render_template('artist.html', all_artist=all_artist)

@app.route('/artist/<artist_id>')
def artist_detail(artist_id): 
    artist_data = Artist.query.get(artist_id)
    return render_template('artist_detail.html', artist=artist_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')

        if role == 'visitor':
            user = Visitor.query.filter_by(name=username, password=password).first()
        else:
            user = Staff.query.filter_by(username=username, password=password).first()

        if user:
            # Bagian paling penting: menyimpan data ke session
            session['user_id'] = user.id
            session['user_name'] = username
            session['role'] = role
            flash(f'Selamat datang, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username atau Password salah!', 'danger')
    
    return render_template('login.html')

# Copas ini juga di bawah fungsi login untuk fitur Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        password = request.form.get('password')

        # 'job' dihilangkan dari sini
        new_v = Visitor(name=name, gender=gender, password=password)
        
        try:
            db.session.add(new_v)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            return "Gagal simpan data"
            
    return render_template('register.html')

@app.route('/profile')
def profile():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    role = session.get('role')
    user_id = session.get('user_id')
    
    if role == 'visitor':
        user_data = Visitor.query.get(user_id)
    else:
        user_data = Staff.query.get(user_id)
        
    return render_template('profile.html', user=user_data, role=role)

@app.route('/all-reviews')
def all_reviews():
    koleksi_art = Art.query.all()
    page_review = InteractionLog.query.filter(
        (InteractionLog.review_art != None)).all()
    return render_template('review.html', all_art=koleksi_art, reviews=page_review)

@app.route('/add-art-review/<int:art_id>', methods=['POST'])
def add_review(art_id):
    r_art = request.form.get('review_art')
    v_id = session.get('user_id') 
    rating = request.form.get('rating')

    print(f"Debug: User ID = {v_id}, Rating = {rating}, Art ID = {art_id}")

    if v_id and rating: 
        new_log = InteractionLog(
            visitor_id=v_id,
            art_id=art_id,
            review_art=r_art,
            rating=int(rating)
        )
        db.session.add(new_log)
        db.session.commit()
        flash('Ulasan berhasil dikirim!', 'success')
    else:
        flash('Gagal kirim review. Pastikan kamu sudah login dan mengisi rating.', 'danger')
        
    return redirect(url_for('all_reviews'))

if __name__ == "__main__":
    app.run(debug=True)
    