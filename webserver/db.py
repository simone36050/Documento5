from typing import Union
from flask import Flask, g
from flaskext.mysql import MySQL
from pymysql.connections import Connection
from pymysql.cursors import Cursor, DictCursor

mysql = MySQL()


# initialization

def init_app(app: Flask):
    # initialize mysql
    mysql.init_app(app)

    # setup function
    app.teardown_appcontext(teardown_g)


def init_g():
    if not hasattr(g, 'mysql'):
        # set g
        g.mysql = mysql
        g.mysql_conn = None
        g.mysql_curs = []

def teardown_g(reponse):
    if (hasattr(g, 'mysql_conn') and 
        g.mysql_conn != None):
        mysql.teardown_request(None)
    return reponse


# user functions

def db_connection():
    init_g()

    if g.mysql_conn != None:
        return g.mysql_conn

    # intialize connection
    conn = g.mysql.get_db()
    g.mysql_conn = conn
    return conn

def db_cursor():
    init_g()

    if g.mysql_conn == None:
        db_connection()

    conn = g.mysql_conn
    curs = conn.cursor(DictCursor)
    g.mysql_curs.append(curs)
    return curs

def database() -> Union[Connection, Cursor]:
    init_g()

    conn = db_connection()
    curs = db_cursor()
    return conn, curs
