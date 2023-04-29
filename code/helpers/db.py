'''!
@package db

Defines a simple decorator to provide a function with a database connection. Afterwards the connection is CLOSED.
'''
from .config import dbname, user, host, password, gssencmode
from psycopg2 import connect
import psycopg2.extensions
from functools import wraps
import datetime

def db_connection(f):
    @wraps(f)
    def wrapped_f(*args,**kwargs):
        conn = connect(f"dbname = {dbname} user = {user} host = {host} password={password} gssencmode = {gssencmode}")
        conn.set_session(readonly=True)
        retval = f(*args, **kwargs, conn=conn)
        conn.close()
        return retval
    return wrapped_f


class CSVCursor(psycopg2.extensions.cursor):
    def __str__(self):
        newline = '\n'
        return f"""\
{ ','.join([a.name for a in self.description]) }
{ newline.join([','.join([item.isoformat() if type(item) == datetime.datetime else str(item) for item in row]) for row in self]) }
"""
