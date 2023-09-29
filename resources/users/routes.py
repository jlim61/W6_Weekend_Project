from flask import request
from uuid import uuid4

from app import app
from db import users, items

@app.get('/user')
def get_users():
    return {'users': users}

@app.post('/user')
def create_user():
    user_data = request.get_json()
    users[uuid4().hex] = user_data
    return user_data, 201


@app.put('/user/<int:user_id>')
def edit_user(user_id):
    user_data = request.get_json()
    try:
        user = users[user_id]
        user['username'] = user_data['username']
        return user, 200
    except KeyError:
        return {'message': 'User not found'}, 400

@app.delete('/user/<user_id>')
def delete_user(user_id):
    try:
        deleted_user = users.pop(user_id)
        return {'message': f'{deleted_user["ign"]} deleted'}, 202
    except:
        return {'message': 'User not found'}, 400

@app.get('/user/<user_id>')
def get_one_user(user_id):
    try:
        user = users[user_id]
        return user, 200
    except:
        return {'message': 'User not found'}, 400
    
@app.get('/user/<user_id>/item')
def get_all_items_from_user(user_id):
    if user_id not in users:
        return {'message': 'User not found'}, 400
    user_items = [item for item in items.values() if item['user_id'] == user_id]
    return user_items, 200