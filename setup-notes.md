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
you make any updates.



when working with sensitive data, create a .gitignore file and enter in any file names. this will ignore them and not
upload them to github.
initial ones to include are .env and your virtual environment folder (the one that is auto populated)