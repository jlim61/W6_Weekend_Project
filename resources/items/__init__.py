from flask_smorest import Blueprint

bp = Blueprint('items', __name__, url_prefix='/item')

from . import routes