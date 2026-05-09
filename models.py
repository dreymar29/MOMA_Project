from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

db = SQLAlchemy()

class Artist(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    biography = db.Column(db.Text)
    arts = db.relationship('Art', backref='author', lazy=True)

class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    artist_id = db.Column(db.String(20), db.ForeignKey('artist.id'))
    audio_path = db.Column(db.String(255), nullable=True) 
    
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    password = db.Column(db.String(100))
    
class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class InteractionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))
    art_id = db.Column(db.Integer, db.ForeignKey('art.id'))
    review_art = db.Column(db.Text, nullable=True)
    review_museum = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    scanned = db.Column(db.Boolean, default=False)
    audio_played = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    art_data = db.relationship('Art', backref='interaction_logs')
    visitor_data = db.relationship('Visitor', backref='logs')