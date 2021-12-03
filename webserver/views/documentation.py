from flask import Blueprint, jsonify, current_app
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint


app = Blueprint('documentation', __name__)

@app.route('/json')
def json():
    return jsonify(swagger(current_app))

swagger_app = get_swaggerui_blueprint(
    '/docs/swagger',
    '/docs/json'
)
