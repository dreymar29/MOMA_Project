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
        job = request.form.get('job')
        pwd = request.form.get('password')

        new_v = Visitor(name=name, gender=gender, job=job, password=pwd)
        db.session.add(new_v)
        db.session.commit()
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/add_review/<int:art_id>', methods=['POST'])
def add_review(art_id):
    try:
        # Ambil data dari form
        text = request.form.get('review_text', '').strip()
        stars = request.form.get('rating')

        # VALIDASI 1: Minimal 10 Kata
        # .split() memecah kalimat jadi daftar kata berdasarkan spasi
        jumlah_kata = len(text.split())
        if jumlah_kata < 10:
            # Jika kurang dari 10, kita "lempar" ke bagian except
            raise ValueError(f"Ulasan minimal 10 kata (punya kamu baru {jumlah_kata} kata).")

        # VALIDASI 2: Rating harus dipilih
        if not stars:
            raise ValueError("Kamu harus memilih rating bintang!")

        # Jika lolos semua validasi, baru simpan ke DB
        new_log = InteractionLog(
            visitor_id=session.get('user_id', 1), # Anggap ID 1 kalau belum login
            art_id=art_id,
            review_text=text,
            rating=int(stars),
            or_status="Reviewed"
        )
        
        db.session.add(new_log)
        db.session.commit()
        flash("Ulasan berhasil dikirim!", "success")

    except ValueError as e:
        # Bagian ini menangkap pesan error dari 'raise ValueError' di atas
        db.session.rollback()
        flash(str(e), "danger") # Mengirim pesan error ke web
        
    except Exception as e:
        # Menangkap error tak terduga (misal database error)
        db.session.rollback()
        flash("Terjadi kesalahan sistem.", "danger")

    return redirect(url_for('art'))

@app.route('/review')
def all_reviews():
    daftar_ulasan = InteractionLog.query.filter(InteractionLog.review_text != None).all()
    return render_template('review.html', reviews=daftar_ulasan)

if __name__ == "__main__":
    app.run(debug=True)
    