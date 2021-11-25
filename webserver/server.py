from flask import Flask, abort, url_for
from database import init_app as db_init_app, database
from config import DebugConfig

app = Flask(__name__)

# config
app.config.from_object(DebugConfig())

# routes

@app.route('/user/<int:id>')
def user_details(id: int):
    _, cur = database()
    sql = """
        SELECT U.firstname, U.lastname, U.username, U.email, U.telephone
        FROM `user` U
        WHERE U.id = %s
    """
    cur.execute(sql, [id])

    if cur.rowcount == 0:
        abort(404)

    return cur.fetchone()

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
    home['user'] = url_for('user_details', id=home['user'], _external=True)
    home['rooms'] = []

    sql = """
        SELECT R.id FROM `room` R
        WHERE R.home = %s
    """
    cur.execute(sql, [id])

    for r in cur.fetchall():
        home['rooms'].append(url_for('room_details', id=r['id'], _external=True))

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
    room['home'] = url_for('home_details', id=room['home'], _external=True)
    room['devices'] = []

    sql = """
        SELECT D.id FROM `device` D
        WHERE D.room = %s
    """
    cur.execute(sql, [id])

    for d in cur.fetchall():
        room['devices'].append(url_for('device_details', id=d['id'], _external=True))

    return room

@app.route('/device/<int:id>')
def device_details(id: int):
    _, cur = database()
    sql = """
        SELECT 
            -- base
                D.name, D.room, 
            -- light
                DL.status,
            -- windows
                DW.status,
            -- alarm
                DA.status,
            -- thermostat
                DT.temperature, DT.umidity
        FROM `device` D
        LEFT JOIN `device_light` DL ON DL.device = D.id
        LEFT JOIN `device_window` DW ON DW.device = D.id
        LEFT JOIN `device_alarm` DA ON DA.device = D.id
        LEFT JOIN `device_thermostat` DT ON DT.device = D.id
        WHERE D.id = %s
    """
    cur.execute(sql, [id])

    if cur.rowcount == 0:
        abort(400)

    result = {}
    for key, value in cur.fetchone().items():
        if key == 'room':
            result[key] = url_for('room_details', id=value, _external=True)
        elif value != None and 'status' in key:
            result[key[3:]] = value
        elif value != None:
            result[key] = value

    return result

@app.route('/device/<int:device>/light/set_status/<string:status>')
def dev_light_set_status(device: int, status: str):
    con, cur = database()

    # check input
    if status not in ['on', 'off']:
        abort(400)

    sql = """
        UPDATE `device_light` DL
        SET DL.status = %s
        WHERE DL.device = %s
    """

    if cur.execute(sql, [status, device]) == 0:
        abort(404)

    con.commit()
    
    return 'OK'

@app.route('/device/<int:device>/window/set_status/<string:status>')
def dev_window_set_status(device: int, status: str):
    con, cur = database()

    # check input
    if status not in ['open', 'close']:
        abort(400)

    sql = """
        UPDATE `device_window` DW
        SET DW.status = %s
        WHERE DW.device = %s
    """

    if cur.execute(sql, [status, device]) == 0:
        abort(404)

    con.commit()
    
    return 'OK'

@app.route('/device/<int:device>/alarm/set_status/<string:status>')
def dev_alarm_set_status(device: int, status: str):
    con, cur = database()

    # check input
    if status not in ['on', 'off']:
        abort(400)

    sql = """
        UPDATE `device_alarm` DA
        SET DA.status = %s
        WHERE DA.device = %s
    """

    if cur.execute(sql, [status, device]) == 0:
        abort(404)

    con.commit()
    
    return 'OK'


@app.route('/device/<int:device>/thermostat/set_temperature/<int:temperature>')
def dev_thermostat_set_temperature(device: int, temperature: int):
    con, cur = database()

    if temperature < 0 or temperature > 40:
        abort(400)

    sql = """
        UPDATE `device_thermostat` DT
        SET DT.temperature = %s
        WHERE DT.device = %s
    """
    
    if cur.execute(sql, [temperature, device]) == 0:
        abort(404)

    con.commit()

    return 'OK'

@app.route('/device/<int:device>/thermostat/set_umidity/<string:umidity>')
def dev_thermostat_set_umidity(device: int, umidity: str):
    con, cur = database()

    # check input
    if umidity not in ['heat', 'cool', 'dry', 'fan']:
        abort(400)

    sql = """
        UPDATE `device_thermostat` DT
        SET DT.umidity = %s
        WHERE DT.device = %s
    """

    if cur.execute(sql, [umidity, device]) == 0:
        abort(404)

    con.commit()
    
    return 'OK'


# run

db_init_app(app)
app.run('0.0.0.0', debug=True)

