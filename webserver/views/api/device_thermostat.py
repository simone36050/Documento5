from flask import Blueprint, abort
from db import database


app = Blueprint('api_device_thermostat', __name__)

@app.route('/device/<int:device>/thermostat/set_temperature/<int:temperature>', methods=['POST'])
def dev_thermostat_set_temperature(device: int, temperature: int):
    """
        Device thermostat new temperature
        ---
        description: Change temperature
        summary: Change thermostat temperature
        tags:
          - thermostat
        responses:
          '200':
            description: Change successfull
          '404':
            description: Device not found
          '400':
            description: Temperature not correct
        parameters:
          - name: id
            in: path
            description: id of the thermostat
            required: true
          - name: temperature
            in: path
            description: new temperature
            required: true  
    """

    con, cur = database()

    if temperature < 10 or temperature > 40:
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

@app.route('/device/<int:device>/thermostat/set_umidity/<string:umidity>', methods=['POST'])
def dev_thermostat_set_umidity(device: int, umidity: str):
    """
        Device thermostat new umidity
        ---
        description: Change umidity
        summary: Change thermostat umidity
        tags:
          - thermostat
        responses:
          '200':
            description: Change successfull
          '404':
            description: Device not found
          '400':
            description: Umidity not correct
        parameters:
          - name: id
            in: path
            description: id of the thermostat
            required: true
          - name: umidity
            in: path
            description: new umidity
            required: true  
    """

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