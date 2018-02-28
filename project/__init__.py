# project/__init__.py
# set APP_SETTINGS=project.config.DevelopmentConfig
# set DATABASE_URL=postgres://postgres:peter926@localhost:5432/users_dev
# set DATABASE_TEST_URL=postgres://postgres:peter926@localhost:5432/users_test
# set SECRET_KEY=change_me
# python manage.py runserver -p 5555
# set REACT_APP_USERS_SERVICE_URL=http://localhost:5555


import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


# instantiate the db
db = SQLAlchemy()
# instantiate flask migrate
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():

    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.api.views import users_blueprint
    from project.api.auth import auth_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
