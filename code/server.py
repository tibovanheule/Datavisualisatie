"""@package server
Provides the api routes. 

More details.
"""

from flask import Flask, send_file, request, Response
from flask_compress import Compress
from flask_cors import CORS, cross_origin
from flask_expects_json import expects_json
from .helpers.db import db_connection, CSVCursor
import datetime
from pathlib import Path

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
            map_month = ["januari", "februari", "maart", "april", "mei", "juni",\
                    "juli", "augustus", "september", "oktober", "november", "december"]
            for i in cur:
                years.append({"year":i[2],"month":map_month[i[1]-1],"result":i[0]})
      
    return (years, 200) if years else ({}, 500)

@app.route('/api/locations', methods=['GET'])
@db_connection
def locations(conn=None):
    """!
    gives back beschikbaarheden
    @return 
    """

    loc_query = "select * from locations;"
    years = []
    if conn is not None:
        with conn.cursor("get data") as cur:
            cur.execute(loc_query,())
            for i in cur:
                years.append(dict(longitude=i[2],latitude=i[1],name=i[3]))
      
    return (years, 200) if years else ({}, 500)

@app.route('/api/parameters', methods=['GET'])
@db_connection
def parameters(conn=None):
    """!
    gives back beschikbaarheden
    @return 
    """

    loc_query = "select locations.location_id, latitude, longitude,locations.naam, series_id,lspi, unit, parameter.naam, parameter.parameter_id from locations join lookup on upper(locations.location_id) = upper(lookup.location_id) join parameter on upper(parameter.parameter_id) = upper(lookup.par);"
    years = []
    if conn is not None:
        with conn.cursor("get data") as cur:
            cur.execute(loc_query,())
            for i in cur:
                years.append(dict(location_id=i[0],latitude=i[1],longitude=[2],location_name=i[3],series_id=i[4],lspi=i[5],unit=i[6],parameter_name=i[7],parameter_id=i[8]))
      
    return (years, 200) if years else ({}, 500)


@app.route('/locations')
def locations_html():
    """!
    Return any file with the given path.
    """
    return send_file('files/locations.html')

@app.route('/beschikbaarheden')
def beschikbaarheden_html():
    """!
    Return any file with the given path.
    """
    return send_file('files/beschikbaarheden.html')

@app.route('/getij')
def getij_html():
    """!
    Return any file with the given path.
    """
    return send_file('files/getij.html')


@app.route('/parameters')
def parameters_html():
    """!
    Return any file with the given path.
    """
    return send_file('files/parameters.html')

@app.route('/wind en golven')
def wind_en_golven_html():
    """!
    Return any file with the given path.
    """
    return send_file('files/wind_en_golven.html')


@app.route('/diep vs ondiep')
def diep_vs_ondiep_html():
    """!
    Return any file with the given path.
    """
    return send_file('files/diep_vs_ondiep_tzw.html')

@app.route('/')
def index_html():
    """!
    Return any file with the given path.
    """
    return send_file('files/index.html')


@app.route('/<path:path>')
def files(path):
    """!
    Return any file with the given path.
    """
    base_loc = Path("./files")
    if (Path(path)).is_file():
        return send_file(Path(path))
    files = list(base_loc.glob(path+"*"))
    print(files)
    if len(files) >0:
        return send_file(files[0])
    if (base_loc/path).is_dir():
        return send_file(base_loc/path/'index.html')
    return Response(status=404)
