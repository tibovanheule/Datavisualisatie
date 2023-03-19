'''!
@package db

Defines a simple decorator to provide a function with a database connection. Afterwards the connection is CLOSED.
'''
from .config import dbname, user, host, password, gssencmode
from psycopg2 import connect

def db_connection():
    db_name = dbname
    def wrap(f):
        def wrapped_f(*args,**kwargs):
            conn = connect(f"dbname = {db_name} user = {user} host = {host} password={password} gssencmode = {gssencmode}")
            conn.set_session(readonly=True)
            retval = f(*args, **kwargs, conn=conn)
            conn.close()
            return retval
        return wrapped_f
    return wrap
