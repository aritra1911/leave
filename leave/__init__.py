import os
from flask import Flask
import click
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object("config")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)

    from . import models

    @app.cli.command('init-db')
    def initdb():
        """Initialize the database."""
        db.drop_all(app=app)
        db.create_all(app=app)
        click.echo('Initialized the database.')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
