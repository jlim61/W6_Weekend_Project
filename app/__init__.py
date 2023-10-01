from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Config import Config

# make an instance of the Flask class (usually default is app)
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate =Migrate(app, db)
api = Api(app)

from resources.users import bp as user_bp
api.register_blueprint(user_bp)
from resources.items import bp as items_bp
api.register_blueprint(items_bp)

from resources.users import routes
from resources.items import routes
from resources.users.UserModel import UserModel
from resources.items.ItemModel import ItemModel