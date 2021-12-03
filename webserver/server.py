from flask import Flask, abort, url_for, render_template, redirect, jsonify
from db import init_app as db_init_app, database
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from config import DebugConfig

app = Flask(__name__)

# config
app.config.from_object(DebugConfig())


# routes user




# routes api










@app.route('/api/device/<int:device>/light/set_status/<string:status>', methods=['POST'])
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

@app.route('/api/device/<int:device>/window/set_status/<string:status>', methods=['POST'])
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

@app.route('/api/device/<int:device>/alarm/set_status/<string:status>', methods=['POST'])
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


# documentation
from views.documentation import app as documentation_app, swagger_app
app.register_blueprint(documentation_app, url_prefix='/docs')
app.register_blueprint(swagger_app)

# base
from views.base import app as base_app
app.register_blueprint(base_app)

# api
from views.api.user import app as api_user_app
from views.api.home import app as api_home_app
from views.api.device import app as api_device_app
from views.api.device_thermostat import app as api_device_thermostat_app

app.register_blueprint(api_user_app, url_prefix='/api')
app.register_blueprint(api_home_app, url_prefix='/api')
app.register_blueprint(api_device_app, url_prefix='/api')
app.register_blueprint(api_device_thermostat_app, url_prefix='/api')

# run

db_init_app(app)
app.run('0.0.0.0', debug=True)

