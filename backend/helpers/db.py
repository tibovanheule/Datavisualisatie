'''!
@package db

Defines a simple decorator to provide a function with a database connection. Afterwards the connection is CLOSED.
'''
from .config import dbname, dbname_lp, user, host, password, gssencmode
from psycopg2 import connect

def db_connection(lspi):
    db_name = dbname
    if lspi == True:
        db_name = dbname_lp
    def wrap(f):
        def wrapped_f(*args,**kwargs):
            conn = connect(f"dbname = {db_name} user = {user} host = {host} password={password} gssencmode = {gssencmode}")
            conn.set_session(readonly=True)
            retval = f(*args, **kwargs, conn=conn)
            conn.close()
            return retval
        return wrapped_f
    return wrap
