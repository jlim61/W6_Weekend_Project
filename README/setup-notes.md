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
pip install 
pip install 
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