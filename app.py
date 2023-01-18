from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from models import setup_db, fill_db, User, Link


# create and configure the app
app = Flask(__name__)
app.app_context().push()
setup_db(app)
fill_db()

CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response



@app.route('/')
def index():
    return jsonify({
        'success': True,
        'message': 'Hello World'
    })

@app.route('/links/<username>')
def get_links(username):
    user = User.query.filter_by(username=username).first()
    # user = User.query.filter_by(id=id).one_or_404()
    if not user:
        abort(404)
    links = Link.query.filter_by(user_id=user.id).all()

    return jsonify({
        'success': True,
        'links': [link.serialize() for link in links]
    })



