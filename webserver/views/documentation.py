from flask import Blueprint, jsonify, current_app
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint


app = Blueprint('documentation', __name__)

@app.route('/json')
def json():
    doc = swagger(current_app)
    doc['info']['version'] = "0.1.0"
    doc['info']['title'] = "MechaHome"
    return jsonify(doc)

swagger_app = get_swaggerui_blueprint(
    '/docs/swagger',
    '/docs/json'
)
