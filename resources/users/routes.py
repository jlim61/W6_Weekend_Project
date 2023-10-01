from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from schemas import DeleteUserSchema, ItemSchema, UpdateUserSchema, UserNestedSchema, UserSchema
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

    # delete a user
    @jwt_required()
    @bp.arguments(DeleteUserSchema)
    def delete(self, user_data):
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)
        if user and user.username == user_data['username'] and user.check_password(user_data['password']):
            user.delete()
            return {'message': f'{user_data["username"]} deleted'}, 202
        abort(400, message='Username od Password Invalid')
  
    # edit a user
    @jwt_required()
    @bp.arguments(UpdateUserSchema)
    @bp.response(200, UserSchema)
    def put(self, user_data):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id, description='User not found')
        if user and user.check_password(user_data['password']):
            try:
                user.from_dict(user_data)
                user.save()
                return user
            except IntegrityError:
                abort(400, message='Username, Email, or IGN already taken')

@bp.route('/user/<user_id>')
class User(MethodView):

    # get a singlular user
    @bp.response(200, UserNestedSchema)
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

@bp.route('/user/friend/<friended_id>')
class AddFriend(MethodView):

    # add to friend list
    @jwt_required()
    @bp.response(200, UserSchema(many=True))
    def post(self, friended_id):
        friending_id = get_jwt_identity()
        user = UserModel.query.get(friending_id)
        friend_to_add = UserModel.query.get(friended_id)
        if user and friend_to_add:
            user.add_friend(friend_to_add)
            return user.friend_list.all()
        abort(400, message='Invalid User Info')

    # unfriend
    @jwt_required()
    def put(self, friended_id):
        friending_id = get_jwt_identity()
        user = UserModel.query.get(friending_id)
        friend_to_remove = UserModel.query.get(friended_id)
        if user and friend_to_remove:
            user.unfriend(friend_to_remove)
            return {'message': f'{friend_to_remove.ign} was removed from your friends list'}
        abort(400, message='Invalid User Info')