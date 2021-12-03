from flask import Blueprint, abort, url_for
from db import database


app = Blueprint('api_device', __name__)


@app.route('/device/<int:id>')
def device_details(id: int):
    """
        Device details
        ---
        description: Device details
        summary: Get device by id
        tags:
          - device
        responses:
          '200':
            description: Device details
          '404':
            description: Device not found
        parameters:
          - name: id
            in: path
            description: id of the device
            required: true  
    """

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
            result[key] = url_for('api_home.room_details', id=value, _external=True)
        elif value != None and 'status' in key:
            result[key[3:]] = value
        elif value != None:
            result[key] = value

    return result