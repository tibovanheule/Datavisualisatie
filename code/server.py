"""@package server
Provides the api routes. 

More details.
"""

from flask import Flask, send_from_directory, request
from flask_compress import Compress
from flask_cors import CORS, cross_origin
from flask_expects_json import expects_json
from .helpers.db import db_connection

app = Flask(__name__)
compress = Compress()
compress.init_app(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/beschikbaarheden', methods=['POST'])
@expects_json({
    'series_id': 'object'
})
@db_connection()
def beschikbaarheden(conn=None):
    """!
    gives back beschikbaarheden
    @return 
    """
    data = request.get_json()
    if len(data) <= 0:
        return ({}, 400)
    
    series_id = data['series_id']
    beschikbaarheden_query = "select percent, month, year from beschikbaarheden(%s)"
    years = {}
    if conn is not None:
        with conn.cursor("get data") as cur:
            cur.execute(beschikbaarheden_query,(series_id,))
            map_month = ["januari", "febuari", "maart", "april", "mei", "juni",\
                    "juli", "augustus", "september", "oktober", "november", "december"]
            for i in cur:
                if i[2] not in years:
                    years[i[2]] = {"jaar":i[2]}
                years[i[2]][map_month[i[1]-1]] = i[0]
            if len(years)>0:
                min_jaar = min(years.keys())
                max_jaar = max(years.keys())
                for i in range(min_jaar,max_jaar+1):
                    if i not in years:
                        years[i[2]] = {"jaar":str(int(i))}        
    return (years, 200) if years else ({}, 500)


@app.route('/beschikbaarheden')
def beschikbaarhedenview():
    """!
    Insert new project in management database
    @return a dict with id and names of waterinfo station.
    """
    return send_from_directory('files',"beschikbaarheden.html")


@app.route('/static/<path:path>')
def doc_files():
    """!
    Insert new project in management database
    @return a dict with id and names of waterinfo station.
    """
    return send_from_directory('files/static', path)
