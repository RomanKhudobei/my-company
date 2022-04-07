import os

from flask import Flask
from sqlalchemy_utils import force_auto_coercion

import auth
from . import exceptions
from .blueprints import register_blueprints
from .db import db
from .db import migrate
from .jwt import jwt
from .marshmallow import ma

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]


def create_app(app_name=PKG_NAME, test_config=None):
    app = Flask(app_name)
    register_blueprints(app)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    force_auto_coercion()
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    exceptions.init_package(app)
    auth.init_package(app)

    # importing models for flask-migrate in order to track models
    from company import models
    from user import models

    return app
