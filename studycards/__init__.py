from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
#from session import Session


app = Flask(__name__)
app.config['SECRET_KEY'] = '345930c09b890a98f09ed574d028ace'
'''SQALCHEMY is set up to use sqlite'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
#session(app)
from studycards import routes




