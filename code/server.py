"""@package server
Provides the api routes. 

More details.
"""

from flask import Flask, send_from_directory, request, Response
from flask_compress import Compress
from flask_cors import CORS, cross_origin
from flask_expects_json import expects_json
from .helpers.db import db_connection, CSVCursor
import datetime

app = Flask(__name__)
compress = Compress()
compress.init_app(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'




@app.route('/api/lspi', methods=['GET'])
@db_connection
def lspi(conn=None):
    """!
    gives back lspi
    @return 
    """
    eenheid_query = "select eenheid, type from eenheden where code = %s"
    lspi_query = "select series_id, lspi from lookup;"
    lspi = []
    if conn is not None:
        with conn.cursor("get data") as cur:
            cur.execute(lspi_query,())
            for i in cur:
                lspi.append({"series_id":i[0],"lspi":i[1]})
      
    return (lspi, 200) if lspi else ({}, 500)

@app.route('/api/beschikbaarheden', methods=['POST'])
@expects_json({
    'series_id': 'object'
})
@db_connection
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
    years = []
    if conn is not None:
        with conn.cursor("get data") as cur:
            cur.execute(beschikbaarheden_query,(series_id,))
            map_month = ["januari", "febuari", "maart", "april", "mei", "juni",\
                    "juli", "augustus", "september", "oktober", "november", "december"]
            for i in cur:
                years.append({"year":i[2],"month":map_month[i[1]-1],"result":i[0]})
      
    return (years, 200) if years else ({}, 500)


@app.route('/api/windsnelheid')
@db_connection
def windsnelheid(conn=None):
    min_date = request.args.get('min_date', type=datetime.datetime.fromisoformat)
    max_date = request.args.get('max_date', type=datetime.datetime.fromisoformat)
    if min_date is None or max_date is None:
        return Response(status=400)

    with conn.cursor(cursor_factory=CSVCursor) as cur:
        cur.execute("""
            SELECT datum, value FROM measurements m INNER JOIN lookup l ON m.series_id=l.series_id 
            WHERE l.par='WVS' AND datum >= %(min_date)s AND datum <= %(max_date)s ORDER BY datum;
        """, { 'min_date': min_date, 'max_date': max_date })
        return str(cur)


@app.route('/api/golfhoogte')
@db_connection
def golfhoogte(conn=None):
    min_date = request.args.get('min_date', type=datetime.datetime.fromisoformat)
    max_date = request.args.get('max_date', type=datetime.datetime.fromisoformat)
    if min_date is None or max_date is None:
        return Response(status=400)
    
    with conn.cursor(cursor_factory=CSVCursor) as cur:
        cur.execute("""
            SELECT datum, value FROM measurements m INNER JOIN lookup l ON m.series_id=l.series_id 
            WHERE l.par='GHA' AND datum >= %(min_date)s AND datum <= %(max_date)s ORDER BY datum;
        """, { 'min_date': min_date, 'max_date': max_date })
        return str(cur)


@app.route('/beschikbaarheden')
def beschikbaarhedenview():
    """!
    Insert new project in management database
    @return a dict with id and names of waterinfo station.
    """
    return send_from_directory('files',"beschikbaarheden.html")


@app.route('/<path:path>')
def doc_files(path):
    """!
    Insert new project in management database
    @return a dict with id and names of waterinfo station.
    """
    return send_from_directory('files', path)
