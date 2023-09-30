from flask import Flask
from flask_smorest import Api
from Config import Config

# make an instance of the Flask class (usually default is app)
app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

from resources.users import bp as user_bp
api.register_blueprint(user_bp)
from resources.items import bp as items_bp
api.register_blueprint(items_bp)

from resources.users import routes
from resources.items import routes