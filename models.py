from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    rgb_texts = db.relationship('RGBText', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class RGBText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text_content = db.Column(db.String(100), nullable=False)
    font_size = db.Column(db.Integer, default=40)
    animation_speed = db.Column(db.Float, default=2.0)
    glow_intensity = db.Column(db.Integer, default=10)
    color_1 = db.Column(db.String(7), default="#ff0000")
    color_2 = db.Column(db.String(7), default="#00ff00")
    color_3 = db.Column(db.String(7), default="#0000ff")
    font_weight = db.Column(db.Integer, default=700)
    letter_spacing = db.Column(db.Integer, default=0)
    shadow_color = db.Column(db.String(7), default="#ffffff")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"RGBText('{self.text_content}', '{self.created_at}')"
