from flask import request
from uuid import uuid4
from flask_smorest import abort
from flask.views import MethodView

from . import bp
from db import users, items


@bp.route('/user')
class UserList(MethodView):

    # get all users
    def get(self):
        return users, 200

    # create a user
    def post(self):
        user_data = request.get_json()
        for k in ['username', 'email', 'password', 'ign']:
            if k not in user_data:
                abort(400, message='Please include username, email and password')
        users[uuid4().hex] = user_data
        return user_data, 201


@bp.route('/user/<user_id>')
class User(MethodView):

    # edit a user
    def put(self, user_id):
        user_data = request.get_json()
        try:
            user = users[user_id]
            user['username'] = user_data['username']
            return user, 200
        except KeyError:
            abort(404, message='User not found')

    # delete a user
    def delete(self, user_id):
        try:
            deleted_user = users.pop(user_id)
            return {'message': f'{deleted_user["ign"]} deleted'}, 202
        except:
            abort(404, message='User not found')

    # get a singlular user
    def get(self, user_id):
        try:
            user = users[user_id]
            return user, 200
        except:
            abort(404, message='User not found')
    
@bp.get('/user/<user_id>/item')
def get_all_items_from_user(user_id):
    if user_id not in users:
        abort(404, message='User not found')
    user_items = [item for item in items.values() if item['user_id'] == user_id]
    return user_items, 200