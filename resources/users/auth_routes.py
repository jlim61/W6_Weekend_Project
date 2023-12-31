from flask_smorest import abort
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from schemas import AuthUserSchema, ItemSchema, UpdateUserSchema, UserNestedSchema, UserSchema, DeleteUserSchema
from . import bp
from .UserModel import UserModel

@bp.post('/register')
@bp.arguments(UserSchema)
@bp.response(201, UserSchema)
def register_account(user_data):
    user = UserModel()
    user.from_dict(user_data)
    try:
        user.save()
        return user_data
    except IntegrityError:
        abort(400, message='Username, Email, or IGN already taken')


@bp.post('/login')
@bp.arguments(AuthUserSchema)
def login(login_info):
    if 'username' not in login_info and 'email' not in login_info:
        abort(400, message='Please include Username or Email')
    if 'username' in login_info:
        user = UserModel.query.filter_by(username=login_info['username']).first()
    else:
        user = UserModel.query.filter_by(email=login_info['email']).first()
    if user and user.check_password(login_info['password']):
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}
    abort(400, message='Invalid Username/Email or Password')


# @bp.route('/logout')