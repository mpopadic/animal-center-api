import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


# Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(os.path.join(basedir, 'db.sqlite3'))

# Init db
db = SQLAlchemy(app)


# Run server
if __name__ == "__main__":
    app.run(debug=True)