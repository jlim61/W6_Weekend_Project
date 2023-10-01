from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError

from resources.users.UserModel import UserModel

from .ItemModel import ItemModel
from schemas import ItemSchema
from . import bp

@bp.route('/')
class ItemList(MethodView):

    # get all items
    @bp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items

    @bp.arguments(ItemSchema)
    @bp.response(200, ItemSchema)
    def post(self, item_data):
       # ** destructures data and gets the keys for associated keys and values for associated keys
       i = ItemModel(**item_data)
       u = UserModel.query.get(item_data['user_id'])
       if u:
          i.save()
          return i
       else:
          abort(400, message="Invalid User Id")

@bp.route('/<item_id>')
class Item(MethodView):

    # get a singular item
    @bp.response(200, ItemSchema)
    def get(self, item_id):
        i = ItemModel.query.get(item_id)
        if i:
            return i
        abort(400, message='Invalid Item ID')

    # edit an item
    @bp.arguments(ItemSchema)
    @bp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        i = ItemModel.query.get(item_id)
        if i and item_data['item_name']:
            if i.user_id == item_data['user_id']:
                i.item_name = item_data['item_name']
                i.description = item_data.get('description', i.description)
                i.price = item_data.get('price', i.price)
                i.save()
                return i
        abort(404, message="Invalid Item Data")

    # delete an item
    def delete(self, item_id):
        req_data = request.get_json()
        user_id = req_data['user_id']
        i = ItemModel.query.get(item_id)
        if i:
            if i.user_id == user_id:
                i.delete()
                return {'message': 'Item Deleted'}, 202
            abort(400, message='User doesn\'t have rights')
        abort(400, message='Invalid Item ID')
        