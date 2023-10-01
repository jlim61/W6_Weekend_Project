from flask import request
from flask_smorest import abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from schemas import DeleteUserSchema, ItemSchema, UpdateUserSchema, UserSchema
from . import bp
from .UserModel import UserModel
from db import users, items


@bp.route('/user')
class UserList(MethodView):

    # get all users
    @bp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users

# create user
    @bp.arguments(UserSchema)
    @bp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel()
        user.from_dict(user_data)
        try:
            user.save()
            return user_data
        except IntegrityError:
            abort(400, message='Username, Email, or IGN already taken')

    # delete a user
    @bp.arguments(DeleteUserSchema)
    def delete(self):
        user_data = request.get_json()
        user = UserModel.query.filter_by(username=user_data['username']).first()
        if user and user.check_password(user_data['password']):
            user.delete()
            return {'message': f'{user_data["username"]} deleted'}, 202
        abort(400, message='Username od Password Invalid')
  

@bp.route('/user/<user_id>')
class User(MethodView):

    # edit a user
    @bp.arguments(UpdateUserSchema)
    @bp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id, description='User not found')
        if user and user.check_password(user_data['password']):
            try:
                user.from_dict(user_data)
                user.save()
                return user
            except IntegrityError:
                abort(400, message='Username, Email, or IGN already taken')



    # get a singlular user
    @bp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id, description='User not found')
        return user
    
@bp.get('/user/<user_id>/item')
@bp.response(200, ItemSchema(many=True))
def get_all_items_from_user(user_id):
    if user_id not in users:
        abort(404, message='User not found')
    user_items = [item for item in items.values() if item['user_id'] == user_id]
    return user_items