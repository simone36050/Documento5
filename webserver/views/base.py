from flask import Blueprint, render_template, redirect, url_for
from db import database

app = Blueprint('base', __name__)

@app.route('/room/<int:id>')
def view_room(id: int):
    return render_template('room.html', id=id)

@app.route('/device/<int:id>')
def user_device(id: int):
    _, cur = database()

    sql = """
        SELECT count(*) `count` FROM `device_thermostat` DT
        WHERE DT.device = %s 
    """
    cur.execute(sql, [id])

    if cur.fetchone()['count'] == 0:
        return 'Dispositivo non ancora supportato, prova con un termostato!'

    return redirect(url_for('base.user_device_thermostat', id=id))

@app.route('/device/thermostat/<int:id>')
def user_device_thermostat(id: int):
    return render_template('thermostat.html', id=id)
