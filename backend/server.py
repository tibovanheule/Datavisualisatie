"""@package server
Provides the api routes. 

More details.
"""
from flask import Flask, send_from_directory

from flask_compress import Compress
from flask_cors import CORS, cross_origin

app = Flask(__name__)
compress = Compress()
compress.init_app(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/static/<path:path>')
def doc_files(path):
    return send_from_directory('static', path)
