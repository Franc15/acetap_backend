from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = os.environ.get('DB_PORT')
DB_HOST = os.environ.get('DB_HOST')

database_path = 'postgresql://{}/{}'.format(''+DB_USER+':'+DB_PASS+'@'+DB_HOST+':'+DB_PORT, DB_NAME)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    db.app = app
    db.init_app(app)
    db.create_all()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    fname = db.Column(db.String(120))
    lname = db.Column(db.String(120))
    email = db.Column(db.String(350), unique=True)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    dob = db.Column(db.Date())
    links = db.relationship('Link', backref='user')

    def __repr__(self):
        return f'<User {self.id}, name: {self.fname, self.lname} email: {self.email} >'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.fname + ' ' + self.lname,
            'email': self.email,
            'gender': self.gender,
            'phone': self.phone,
            'dob': self.dob
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()


class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(500))
    url = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url
        }

    


