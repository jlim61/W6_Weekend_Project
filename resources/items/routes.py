from flask import request
from uuid import uuid4
from flask_smorest import abort
from flask.views import MethodView

from . import bp
from db import items

@bp.get('/')
class ItemList(MethodView):

    # get all items
    def get(self):
        return {'items': items}

    # create an item
    def post(self):
        item_data = request.get_json()
        if 'item_name' not in item_data or "user_id" not in item_data:
            abort(400, message='Please include item name and user id')
        items[uuid4().hex] = item_data
        return item_data, 201

@bp.route('/<item_id>')
class Item(MethodView):

    # edit an item
    def put(self, item_id):
        item_data = request.get_json()
        if item_id in items:
            item = items[item_id]
            item['item_name'] = item_data['item_name']
            return item['item_name'], 200
        abort(404, message='Item not found')

    # delete an item
    def delete(self, item_id):
        try:
            deleted_item = items.pop(item_id)
            return {'message': f'{deleted_item["item_name"]} deleted'}, 202
        except:
            abort(404, message='Item not found')

    # get a singular item
    def get(self, item_id):
        try:
            item = items[item_id]
            return item, 200
        except:
            abort(404, message='Item not found')
