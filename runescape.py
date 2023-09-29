from flask import Flask

# make an instance of the Flask class (usually default is app)
app = Flask(__name__)

@app.route('/index')
def index():
    return