from flask_smorest import Blueprint

bp = Blueprint('items', __name__, url_prefix='/item', description='Ops on Items')

from . import routes