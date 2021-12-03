from flask import Blueprint, abort, url_for
from db import database


app = Blueprint('api_home', __name__)


@app.route('/home/<int:id>')
def home_details(id: int):
    _, cur = database()
    sql = """
        SELECT H.user, H.name FROM `home` H
        WHERE H.id = %s
    """
    cur.execute(sql, [id])
    
    if cur.rowcount == 0:
        abort(404)

    home = cur.fetchone()
    home['user'] = url_for('api_user.user_details', id=home['user'], _external=True)
    home['rooms'] = []

    sql = """
        SELECT R.id FROM `room` R
        WHERE R.home = %s
    """
    cur.execute(sql, [id])

    for r in cur.fetchall():
        home['rooms'].append(url_for('api_home.room_details', id=r['id'], _external=True))

    return home


@app.route('/room/<int:id>')
def room_details(id: int):
    _, cur = database()
    sql = """
        SELECT R.home, R.name FROM `room` R
        WHERE R.id = %s
    """
    cur.execute(sql, [id])

    if cur.rowcount == 0:
        abort(404)

    room = cur.fetchone()
    room['home'] = url_for('api_home.home_details', id=room['home'], _external=True)
    room['devices'] = []

    sql = """
        SELECT D.name, D.id FROM `device` D
        WHERE D.room = %s
    """
    cur.execute(sql, [id])

    for d in cur.fetchall():
        room['devices'].append({ 'name': d['name'], 'id': d['id'] })

    return room

