import os
from flask import Flask

from database import db
from config import settings


def create_app():
    # Init app
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))

    app.config['SECRET_KEY'] = settings.get('settings', 'secret_key')


    # Database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_name = settings.get('db', 'db_name')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(os.path.join(basedir, db_name))

    # Init db
    db.init_app(app)

    with app.app_context():
        from routes import center, animal, species
        from models import AccessRequest, Animal, Center, Species
        db.create_all()

    app.run()


def create_test_app():
    # Init app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.get('settings', 'secret_key')

    # Database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    db.init_app(app)
    app.app_context().push() # this does the binding
    return app


if __name__ == "__main__":
    create_app()
