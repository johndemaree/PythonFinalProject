from flask import Flask
app = Flask(__name__)
app.Config['SECRET_KEY'] = '345930c09b890a98f09ed574d028ace'

from studycards import routes





