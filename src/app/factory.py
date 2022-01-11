import os

from flask import Flask

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]


def create_app(app_name=PKG_NAME, test_config=None):
    app = Flask(app_name)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    return app
