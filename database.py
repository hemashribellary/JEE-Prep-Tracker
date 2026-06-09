from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    subject = db.Column(db.String(50))
    topic = db.Column(db.String(100))
    questions_attempted = db.Column(db.Integer)
    questions_correct = db.Column(db.Integer)
    time_spent = db.Column(db.Integer)
    notes = db.Column(db.Text)

class Mistake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    subject = db.Column(db.String(50))
    topic = db.Column(db.String(100))
    question = db.Column(db.Text)
    mistake_type = db.Column(db.String(50))
    notes = db.Column(db.Text)
    
