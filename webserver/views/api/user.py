from flask import Blueprint, abort
from db import database


app = Blueprint('api_user', __name__)

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
