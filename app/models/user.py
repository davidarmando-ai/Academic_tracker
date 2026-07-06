from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(256), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship('Task', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    calendar_events = db.relationship('CalendarEvent', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    study_goals = db.relationship('StudyGoal', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
