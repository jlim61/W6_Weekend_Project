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
pip install flask-sqlalchemy      -> sqlalchemy
pip install flask-migrate      -> migrate
pip install psycopg2      -> psycopg2 
pip install flask-jwt-extended      -> flask-jwt-extended

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

================================================================================================
Moving on to Schemas

make a schemas.py file. This will utilize marshmallow so you will need to run the following:
from marshmallow import schema, fields

in a schema, you are defining what fields are needed. additionally there is dump_only and load_only.
dump_only says that it will only give out this info, it doesn't take in.
load_only says that it will only take in this info, it doesn't give out. (think passwords, it will take it in but not give it out)

general example:
class PostSchema(Schema):
    id = fields.Str(dump_only=True)
    item_name = fields.Str(required=True)
    user_id = fields.Str(required=True)

after making a schema, you can start decorating the methods with bp.arguments to take something in (as some fields in the schema are required) and you can also decorate with bp.response to send information out.
remember, @bp.arguments is validating the info we put in. so if our schema is requiring a username and password, if they only put username, it won't work. the @bp.response gives back that information from the schema.

Once responses have been added. we can create elephantsql database so that we can take in data and not lose it upon a new session. once created, you will need to get the URL. then you want to put that in your .env file. you can do that by setting
SQL_DATABASE_URL =<url> but, you will need to at ql in the url
Then in config file, you will need to set the sqlalchemy to get that database. you will need to import os and then:
SQLALCHEMY_DATABASE_URI = os.environ.get('SQL_DATABASE_URL')
Then you will need to pip install flask-sqlalchemy and flask-migrate
Now you will have to instantiate this inside the app init file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate =Migrate(app, db) -> it needs to take in db

then we can start working on making model pages. so for each specific table folder (in this case user and items) make a UserModel and ItemModel file

in UserModel, you can from app import db to get the database.
each attribute in this class UserModel(db.Model)
is going to be a column in our table. Once you have set up all the columns and made whichever ones nullable and not, install:
pip install psycopg2

to securely hash a password:
from werkzeug.security import generate_password_hash, check_password_hash

to connect to elephantsql database, run these:
flask db init -> add the migrations folder that generates to .gitignore
flask db migrate -m "first migrate" -> it's like the add. and commit in github
flask db upgrade -> this is the push, without this you wont' see your tables in elephantsql

now that we are connected, we can update some of the routes. we won't need to uuid4 anymore because we are going to be using werkzeug to hash the passwords.
to send things, you need to make in the model page a save function:
a save function to send it to the database and a delete function to remove it off the database
   def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

When making a model for something that has a foreign key such as item in this case. The item, you have a user id coming from users. Look at the ItemModel to see how you would reference a foreignkey.
from app import db

class ItemModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

Additionally, we can create a link on the UserModel for items. This would give all the items owned by the user. Review the items =db.relationship line as that shows how to do it. The backref uses that key word to allow you to see all their items.
class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    ign = db.Column(db.String, unique=True, nullable=False)
    items = db.relationship('ItemModel', backref='author', lazy='dynamic', cascade='all, delete')

    you can then run flask db migrate -m'message and flask db upgrade to add the item table.
    if the info doesn't match for the datatype, it can give you an error. Try running flask db downgrade, flask db stamp head, flask db heads
    because you might be getting errors trying to upgrade or on the migrate saying you're not up to date

    now that table for items has been conncted to elephantsql, you can adjust the routes for items.


============================================================================================
Adding Adding Friend Routes (Many to Many Route)

first, you will need to create a table for this as it will start needing it's own friending and friended ids. See example below:

friends = db.Table('friends',
    db.Column('friending_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('friended_id', db.Integer, db.ForeignKey('users.id'))
)

Also need to add the relationship to the UserModel:
class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    ign = db.Column(db.String, unique=True, nullable=False)
    items = db.relationship('ItemModel', backref='author', lazy='dynamic', cascade='all, delete')
    friend_list = db.relationship('UserModel', secondary=friends,
        primary_join = friends.friending_id == id,
        secondary_join = friends.friended_id == id,
        backref = db.backref('friends', lazy='dynamic'),
        lazy='dynamic'
    )

================================================================================================================
access-token and security

first we must pip install flask-jwt-extended and then add it to our app init file
then you need to add to our  Config: JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
remember to add the real value in the .env file so that it doesn't get shown on github.
to generate the real secret key for .env file go into python though terminal by running the following:
>python
>from secrets import SystemRandom
>SystemRandom().getrandbits(128)

copy the number and enter into .env: JWT_SECRET_KEY=number

can also set up separate files for users called auth_routes. these can contain user registration, login and logout. the registration is really a create user so you can cut that from the regular routes and move it to auth routs.