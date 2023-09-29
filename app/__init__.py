from flask import Flask

# make an instance of the Flask class (usually default is app)
app = Flask(__name__)

from resources.users import routes
from resources.items import routes