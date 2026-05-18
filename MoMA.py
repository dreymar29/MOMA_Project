from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import db, Art, Artist, Visitor, Staff, InteractionLog
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_moma'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'moma.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Konfigurasi Upload Folder
UPLOAD_FOLDER = os.path.join(basedir, 'static/image')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_IMAGE = {'png', 'jpg', 'jpeg', 'webp'}
ALLOWED_AUDIO = {'mp3'}

def allowed_file(filename, extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions

@app.route('/')
def index():
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
            user = Staff.query.filter_by(name=username, password=password).first()

        if user:
            # Bagian paling penting: menyimpan data ke session
            session['user_id'] = user.id
            session['user_name'] = username
            session['role'] = role
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid Username or Password!', 'danger')
    
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
            return "Failed to save data"
            
    return render_template('register.html')

@app.route('/profile')
def profile():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    role = session.get('role')
    user_id = session.get('user_id')
    
    if role == 'visitor':
        user_data = Visitor.query.get(user_id)
        user_logs = InteractionLog.query.filter_by(visitor_id=user_id).order_by(InteractionLog.timestamp.desc()).all()
        last_activity = user_logs[0].timestamp if user_logs else "Belum ada aktivitas"
    else:
        user_data = Staff.query.get(user_id)
        user_logs = []
        last_activity = "N/A"
        
    return render_template('profile.html', user=user_data, role=role, logs=user_logs, last_active=last_activity)

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
        flash('Review submitted successfully!', 'success')
    else:
        flash('Failed to submit review. Please ensure you are logged in and provided a rating.', 'danger')
        
    return redirect(url_for('all_reviews'))

@app.route('/edit-review/<int:log_id>', methods=['GET', 'POST'])
def edit_review(log_id):
    review = InteractionLog.query.get_or_404(log_id)
    
    if request.method == 'POST':
        review.review_art = request.form.get('review_art')
        review.rating = int(request.form.get('rating'))
        db.session.commit()
        flash('Review updated successfully!', 'success')
        return redirect(url_for('profile'))
        
    return render_template('edit_review.html', review=review)

@app.route('/delete-review/<int:log_id>')
def delete_review(log_id):
    review = InteractionLog.query.get_or_404(log_id)
    
    if session.get('user_id') == review.visitor_id:
        db.session.delete(review)
        db.session.commit()
        flash('Review deleted successfully.', 'success')
    
    return redirect(url_for('profile'))

# --- FITUR CRUD STAFF ---

@app.route('/staff/manage-art')
def manage_art():
    if session.get('role') != 'staff':
        flash('Access denied! Staff only.', 'danger')
        return redirect(url_for('index'))
    arts = Art.query.all()
    return render_template('manage_art.html', arts=arts)

@app.route('/staff/add-art', methods=['GET', 'POST'])
def add_art():
    if session.get('role') != 'staff':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Ambil data dari form
        artist_name = request.form.get('artist_name')
        biography = request.form.get('biography')
        art_name = request.form.get('art_name')
        description = request.form.get('description')
        
        f_artist_photo = request.files.get('photo_artist')
        f_art_photo = request.files.get('photo_art')
        f_audio = request.files.get('audio_file')

        # Handle Artist (Gunakan yang sudah ada atau buat baru)
        artist = Artist.query.filter_by(name=artist_name).first()
        if not artist:
            # Gunakan ID artist jika diinput atau generate jika tidak (asumsi serial 9 digit)
            artist_id_input = request.form.get('artist_id')
            if not artist_id_input:
                artist_id_input = str(uuid.uuid4().int)[:9]
            
            artist = Artist(id=artist_id_input, name=artist_name, biography=biography)
            db.session.add(artist)

        # Upload Foto Artist dinamai berdasarkan artist.id
        if f_artist_photo and allowed_file(f_artist_photo.filename, ALLOWED_IMAGE):
            ext = f_artist_photo.filename.rsplit('.', 1)[1].lower()
            fname = f"{artist.id}.{ext}"
            f_artist_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            artist.photo_path = fname

        # Buat Objek Art baru (Tanpa ID dulu jika auto-increment)
        new_art = Art(name=art_name, description=description, author=artist)
        db.session.add(new_art)
        db.session.flush() # Mengambil ID dari database sebelum commit final
        
        # Upload Foto Art dinamai berdasarkan art.id
        if f_art_photo and allowed_file(f_art_photo.filename, ALLOWED_IMAGE):
            ext = f_art_photo.filename.rsplit('.', 1)[1].lower()
            fname = f"{new_art.id}.{ext}"
            f_art_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            new_art.image_path = fname
            
        # Upload Audio dinamai berdasarkan art.id
        if f_audio and allowed_file(f_audio.filename, ALLOWED_AUDIO):
            fname = f"{new_art.id}.mp3"
            f_audio.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            new_art.audio_path = fname

        db.session.commit()
        flash('Art successfully added!', 'success')
        return redirect(url_for('manage_art'))
    
    return render_template('add_art.html')

@app.route('/staff/edit-art/<int:art_id>', methods=['GET', 'POST'])
def edit_art(art_id):
    if session.get('role') != 'staff':
        return redirect(url_for('login'))
    
    art = Art.query.get_or_404(art_id)
    if request.method == 'POST':
        art.name = request.form.get('art_name')
        art.description = request.form.get('description')
        
        # Update file foto jika ada unggahan baru
        f_art_photo = request.files.get('photo_art')
        if f_art_photo and allowed_file(f_art_photo.filename, ALLOWED_IMAGE):
            fname = secure_filename(f"art_upd_{art.id}_{f_art_photo.filename}")
            f_art_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            art.image_path = fname
            
        db.session.commit()
        flash('Data updated successfully!', 'success')
        return redirect(url_for('manage_art'))
        
    return render_template('edit_art.html', art=art)

@app.route('/staff/delete-art/<int:art_id>')
def delete_art(art_id):
    if session.get('role') != 'staff': return redirect(url_for('login'))
    art = Art.query.get_or_404(art_id)
    db.session.delete(art)
    db.session.commit()
    flash('Art deleted successfully.', 'success')
    return redirect(url_for('manage_art'))

# --- FITUR CRUD ARTIST ---

@app.route('/staff/manage-artists')
def manage_artists():
    if session.get('role') != 'staff':
        flash('Access denied! Staff only.', 'danger')
        return redirect(url_for('index'))
    artists = Artist.query.all()
    return render_template('manage_artists.html', artists=artists)

@app.route('/staff/edit-artist/<artist_id>', methods=['GET', 'POST'])
def edit_artist(artist_id):
    if session.get('role') != 'staff':
        return redirect(url_for('login'))
    artist = Artist.query.get_or_404(artist_id)
    if request.method == 'POST':
        artist.name = request.form.get('name')
        artist.biography = request.form.get('biography')
        
        f_photo = request.files.get('photo')
        if f_photo and allowed_file(f_photo.filename, ALLOWED_IMAGE):
            ext = f_photo.filename.rsplit('.', 1)[1].lower()
            fname = f"{artist.id}.{ext}"
            f_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            artist.photo_path = fname
            
        db.session.commit()
        flash('Artist updated successfully!', 'success')
        return redirect(url_for('manage_artists'))
    return render_template('edit_artist.html', artist=artist)

@app.route('/staff/delete-artist/<artist_id>')
def delete_artist(artist_id):
    if session.get('role') != 'staff': return redirect(url_for('login'))
    artist = Artist.query.get_or_404(artist_id)
    if artist.arts:
        flash('Cannot delete artist who still has art works in collection!', 'danger')
        return redirect(url_for('manage_artists'))
    db.session.delete(artist)
    db.session.commit()
    flash('Artist deleted successfully.', 'success')
    return redirect(url_for('manage_artists'))

@app.route('/search')
def search():
    query = request.args.get('q') 
    if not query:
        return redirect(url_for('index'))

    results_art = Art.query.filter(Art.name.contains(query)).all()
    results_artist = Artist.query.filter(Artist.name.contains(query)).all()
    return render_template('search_results.html', query=query, arts=results_art, artists=results_artist)

if __name__ == "__main__":
    app.run(debug=True)
    