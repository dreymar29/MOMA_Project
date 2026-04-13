from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

db = SQLAlchemy()

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    arts = db.relationship('Art', backref='artist_data', lazy=True)

class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    job = db.Column(db.String(100))
    password = db.Column(db.String(100))
    
class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class InteractionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))
    art_id = db.Column(db.Integer, db.ForeignKey('art.id'))
    review_text = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    art = db.relationship('Art', backref='interaction_logs')
    visitor = db.relationship('Visitor', backref='interaction_logs')
    or_status = db.Column(db.String(50))
    audio_status = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime)