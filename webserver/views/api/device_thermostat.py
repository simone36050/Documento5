from flask import Blueprint, abort
from db import database


app = Blueprint('api_device_thermostat', __name__)

@app.route('/device/<int:device>/thermostat/set_temperature/<int:temperature>', methods=['POST'])
def dev_thermostat_set_temperature(device: int, temperature: int):
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