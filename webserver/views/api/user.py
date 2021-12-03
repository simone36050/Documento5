from flask import Blueprint, abort
from db import database


app = Blueprint('api_user', __name__)

@app.route('/user/<int:id>')
def user_details(id: int):
    """
        Retrive user details
        ---
        description: User details
        summary: Find User by his id
        tags:
          - user
        responses:
          '200':
            description: User details
          '404':
            description: User not found
        parameters:
          - name: id
            in: path
            description: id of the user
            required: true  
    """

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

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    """
        Delete user
        ---
        description: Delete user
        summary: Delete user by his id
        tags:
          - user
        responses:
          '200':
            description: Cancelled successfull
          '404':
            description: User not found
        parameters:
          - name: id
            in: path
            description: id of the user
            required: true  
    """
    pass

@app.route('/user', methods=['POST'])
def add_user(id: int):
    """
        Add user
        ---
        description: Add new user
        summary: New user
        tags:
          - user
        responses:
          '200':
            description: Created successfull
          '403':
            description: Data not corrent
        parameters:
          - name: id
            in: path
            description: id of the user
            required: true  
    """
    pass

