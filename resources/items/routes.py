from flask import request
from uuid import uuid4

from app import app
from db import items

@app.get('/item')
def get_item():
    return {'items': items}

@app.post('/item')
def create_item():
    item_data = request.get_json()
    items[uuid4().hex] = item_data
    return item_data, 201

@app.put('/item/<item_id>')
def edit_item(item_id):
    item_data = request.get_json()
    if item_id in items:
        item = items[item_id]
        item['item_name'] = item_data['item_name']
        return item['item_name'], 200
    return {'message': 'Item not found'}, 404

@app.delete('/item/<item_id>')
def delete_item(item_id):
    try:
        deleted_item = items.pop(item_id)
        return {'message': f'{deleted_item["item_name"]} deleted'}, 202
    except:
        return {'message': 'Item not found'}, 400

@app.get('/item/<item_id>')
def get_one_item(item_id):
    try:
        item = items[item_id]
        return item, 200
    except:
        return {'message': 'Item not found'}, 400