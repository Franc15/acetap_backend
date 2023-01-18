from flask import Flask, jsonify, request
from flask_cors import CORS

from models import setup_db


# create and configure the app
app = Flask(__name__)
app.app_context().push()
setup_db(app)

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


