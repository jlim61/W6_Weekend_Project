from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from resources.users.UserModel import UserModel

from .ItemModel import ItemModel
from schemas import ItemSchema
from . import bp

@bp.route('/')
class ItemList(MethodView):

    # get all items
    @jwt_required()
    @bp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items

    # creating an item
    @jwt_required()
    @bp.arguments(ItemSchema)
    @bp.response(200, ItemSchema)
    def post(self, item_data):
       user_id = get_jwt_identity()
       # ** destructures data and gets the keys for associated keys and values for associated keys
       i = ItemModel(**item_data, user_id=user_id)
       try:
          i.save()
          return i
       except IntegrityError:
          abort(400, message="Invalid User Id")

@bp.route('/<item_id>')
class Item(MethodView):

    # get a singular item
    @jwt_required()
    @bp.response(200, ItemSchema)
    def get(self, item_id):
        i = ItemModel.query.get(item_id)
        if i:
            return i
        abort(400, message='Invalid Item ID')

    # edit an item
    @jwt_required()
    @bp.arguments(ItemSchema)
    @bp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        i = ItemModel.query.get(item_id)
        if i and item_data['item_name']:
            user_id = get_jwt_identity()
            if i.user_id == user_id:
                i.item_name = item_data['item_name']
                i.description = item_data.get('description', i.description)
                i.price = item_data.get('price', i.price)
                i.save()
                return i
            else:
                abort(401, message='Unauthorized')
        abort(404, message="Invalid Item Data")

    # delete an item
    @jwt_required()
    def delete(self, item_id):
        user_id = get_jwt_identity()
        i = ItemModel.query.get(item_id)
        if i:
            if i.user_id == user_id:
                i.delete()
                return {'message': 'Item Deleted'}, 202
            abort(401, message='User doesn\'t have rights')
        abort(400, message='Invalid Item ID')
        