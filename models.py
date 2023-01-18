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
    db.drop_all()
    db.create_all()

def fill_db():
    user1 = User(fname='John', lname='Doe', email='johndoe@gmail.com', gender='male',
        username='john.doe', phone='1234567890', dob='1990-2-10')
    user2 = User(fname='Jane', lname='Doe', email='janedoe@gmail.com', gender='female',
        username='jane.doe', phone='1234567890', dob='1992-1-1')
    user3 = User(fname='Francis', lname='Kikulwe', email='francis@gmail.com', gender='male',
        username='franc.kikulwe', phone='54879046', dob='1998-11-9')
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    link1 = Link(title='Facebook', url='https://www.facebook.com/johndoe', user=user1)
    link2 = Link(title='Twitter', url='https://www.twitter.com/johndoe', user=user1)
    link3 = Link(title='Facebook', url='https://www.facebook.com/janedoe', user=user2)
    link4 = Link(title='Twitter', url='https://www.twitter.com/janedoe', user=user2)
    link5 = Link(title='Facebook', url='https://www.facebook.com/francis', user=user3)
    link6 = Link(title='Twitter', url='https://www.twitter.com/francis', user=user3)
    link7 = Link(title='LinkedIn', url='https://www.linkedin.com/francis', user=user3)
    link8 = Link(title='Github', url='https://www.github.com/francis', user=user3)
    link9 = Link(title='LinkedIn', url='https://www.linkedin.com/johndoe', user=user1)
    link10 = Link(title='Github', url='https://www.github.com/johndoe', user=user1)
    link11 = Link(title='LinkedIn', url='https://www.linkedin.com/janedoe', user=user2)
    link12 = Link(title='Github', url='https://www.github.com/janedoe', user=user2)
    db.session.add_all([link1, link2, link3, link4, link5, link6, link7, link8, link9, link10, link11, link12])
    db.session.commit()
    

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    fname = db.Column(db.String(120))
    lname = db.Column(db.String(120))
    username = db.Column(db.String(120), unique=True)
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

    


