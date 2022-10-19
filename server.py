# Imports
import sqlite3
import flask as flask
from flask import render_template as rt
import flask_sqlalchemy as fsql

# Root Configuration 
root = flask.Flask(__name__)

# Database Connection with Root
root.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storage.db"

# Creation of Database
database = fsql.SQLAlchemy(root)

# Initialisation of App
database.init_app(root)

# Creating the Columns inside the Database
class ContactStorage(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name =  database.Column(database.String(20), unique=True, nullable=False)
    ctnumber =  database.Column(database.Integer, unique=True, nullable=False)
    email_address = database.Column(database.String(30), unique=True, nullable=False)

# Creation of Database with the root.app_context() function.
with root.app_context():
    database.create_all()

# Connection of Database with the server.py file to retrieve values
def get_db_connection():
    conn = sqlite3.connect('storage.db')
    conn.row_factory = sqlite3.Row
    return conn

# Routing the Root to the home page URL - '/' 
@root.route('/', methods=["GET", "POST"])
def home():
    # Retrieving the data from the form and adding it to the Database
    if flask.request.method == "POST":
        # Global Variable
        global data
        # List of Data
        data = ContactStorage(
            name = flask.request.form['name'],
            ctnumber = flask.request.form['ctnumber'],
            email_address = flask.request.form['email']
        )
        # Adding the Data to DAtabase
        database.session.add(data)
        database.session.commit()

        # Returning Redirect
        return flask.redirect('/')

    #Getting the data from the Database 
    conn = get_db_connection()
    cts = conn.execute('SELECT * FROM contact_storage').fetchall()
    conn.close()
    # Returning the data and the render template
    return rt("index.html", title='Home', cts=cts)

# Conditional Preprocessing statement to run the Root
if __name__ == "__main__":
    root.run(debug=True)

