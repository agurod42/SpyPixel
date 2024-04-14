from src import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    spy_pixels = db.relationship('SpyPixel', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Role {}>'.format(self.name)

class SpyPixel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    logs = db.relationship('Log', backref='spy_pixel', lazy=True)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spy_pixel_id = db.Column(db.Integer, db.ForeignKey('spy_pixel.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    ip = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(255), nullable=False)
    data = db.Column(db.JSON, nullable=False)
