Setting up virtual environment
python -m venv <'name of virtual environment'>

activate virtual environment
<'name of virtual environment'>\Scripts\activate


after ANY pip install, run: pip freeze > requirements.txt (this will save the pips that have been installed to a text file)
if somehow pips are removed but you have the list of pips somewhere else, make a requirements.txt file, and then run: pip install -r requirements.txt (any pip in the file will be installed)
if want to see what pips installed, run: pip list

pips installed
pip install flask     -> installing flask
pip install python-dotenv     -> installing python-dotenv
pip install marshmallow      -> installing marshmallow
pip install flask-smorest      -> installing flask-smorest
pip install 
pip install 
pip install 
pip install 

Flask by default looks at app.py. if i rename the file to something else like heroesvillains.py
have to set it in the terminal to have it look to the other file by running: set FLASK_APP=<'file name>
in this case it would be: set FLASK_APP=heroesvillains.py


****NOTE*****
using set FLASK_APP= is not consistent among terminals. once you close the terminal, it will not work. you would need to
install another library: python-dotenv. Make a .env file and you can set the FLASK_APP to that file name.
FLASK_APP=heroesvillains.py

You will also want to update this to have debug mode set to on or else you will have to keep shutting down the server if 
you make any updates. in .env put: FLASK_DEBUG=1



when working with sensitive data, create a .gitignore file and enter in any file names. this will ignore them and not
upload them to github.
initial ones to include are .env and your virtual environment folder (the one that is auto populated)


Start working on creating your first flask end point. This will be denoted by @ (decorator) and tie it to the instance
in this case @app. and then you have to choose what you are doing (POST, GET, ROUTE, etc.). in this case choose route
and then you have to pass the endpoint: @app.route('/index) and then you will have to run a "def"

for initial testing, create a db.py and you can use that to test. When testing, it will be better to create an insomnia collection. Create a collection in insomnia with a related name.

Now start creating CRUD operations. These are basic operations like GET/POST/PUT/DELETE or think about it as
GET/CREATE/EDIT/DELETE. You will need to set an end point for these and each one will run a different function. You can start
off doing these all in the main.py file (runescape.py), but eventually you can break them off into their own separate files.
Set up a resources folder. in there make another folder for each "table" -> in this case it's "users" and "items".
inside the specific folders, set up a routes folder. you can also move the initial database info that you are testing with and move it into a db.py file.

when importing libraries and instantiating them, make an __init__ file. Make an app folder and make an __init__ file in there. The __init__ file makes it a subdirectory. If there a folder with __init__ file, if we import that folder it will run that file.

Next, inside each specific folder (in this case it's users and items) make it's own __init__ file. This will serve as a blueprint for each folder.

====================================================================================
Just finished CRUD Operations without MethodView

Now you can use MethodView if you want.
First pip install marshmallow and flask-smorest. marshmallow validates and serializes data as it is coming to and from our routes. if user is signing up or we are posting a user, we are expecting them to have a username, email, and password. can use marshmallow to make a schema so if they are going to hit this route, they need this information and datatype.

flask smorest works on top of marshmallow. it improves how we are validating and serializing data. flask smorest is more for robust documenation automatically by utilizing marshmallow. we know what information we are expecting, we are using flask smorest to get a well built documentation that we don't have to build.

We should have empty __init__ files. Now we can "from flask import Blueprint" and in that file, we set a variable (i use bp for blueprint) and set it to an instance of Blueprint: bp = Blueprint('<blueprint name>', __name__) -> in this case:
bp = Blueprint('<users>', __name__); there is an optional third argument, it is added to items but not in users for this example. then we have to import routes into the init file from the routes tied to it (in users case, import routes from users). Previously, we were using app to run the functions but now you can replace every instance of app in @app to @bp to use the users blueprint. now you have to import it into the app init file. so you would do from.resources.users import bp (as user_bp). if you have multiple bp, then you can alias them which is what is in the parenthesis. then you have to register it with flask instance. so in this example it might look like:
from resources.users import bp as user_bp
app.register_blueprint(user_bp)

now you can set up the same thing for the items or other folder __init__ files you have. for the item __init__ we are adding the third optional argument which is bp = Blueprint('items', __name__, url_prefix='/item') -> url_prefix='/item'
any route registered with this bp automatically goes to /post

flask_smorest has an abort function that you can import. it is useful in handling error cases and returning appropriate HTTP responses to client when something goes wrong in the api. so if there are any return {error messages} that are being used, you can replace them with abort(code, message="enter message") --> abort(400, message='Item not found')

======================================================================================
Implementing MethodView - rearranging routes

You can start by grouping your CRUD operations together based on endpoints. for example, get all users and create a user follow endpoint "/user". they can be grouped together. Then you assign the bp decorator to a class and make those CRUD operations methods within that class. this also allows you to make the name of the method, what the method is. for example, def create_user() would become def post(). the decorator assigned to the class should be a route, i.e. @bp.route(MethodView)

all the routes are now methods so make sure to add self as an argument. Additionally, you will need to update your __init__ files that are the blueprints. instead of from flask import Blueprint, do from flask_smorest import Blueprint. This should allow it to work. Additionally, you can add a description as an argument to the bp now for further documentation like:
description='Ops on Users'

Next, instantiate flask_app to another third party library. follow this import inside app folder init file:
from flask_smorest import Api
api = Api(app)

update the register blueprints in app init file from app to api as well.

Then you can start making a Config file. You can do this in the app __init__ file instead, but to avoid clutter, it might be better to have a Config.py file with a class Config in it.
everything in the class will be caps lock:
    PROPAGATE_EXCEPTIONS = True -> if we get errors, it will send it to our flask app so it's easier to debug
    API_TITLE = 'Runescape Rest Api'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'  -> THIS IS THE FLASK_SMOREST VERSION
    OPENAPI_URL_PREFIX ='/'
    OPENAPI_SWAGGER_UI_PATH = '/' -> for landing page
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

then go back to app __init__ and from Config import Config. THen in between where you set app and api, make one in the middle: app.config.from_object(Config)