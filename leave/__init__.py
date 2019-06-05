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

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import auth
    app.register_blueprint(auth.bp)

    from .masters import employee, organization
    app.register_blueprint(employee.bp)
    app.register_blueprint(organization.bp)

    from . import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    @app.cli.command('init-db')
    def initdb_command():
        """Initialize the database."""
        from . import models
        db.drop_all(app=db.get_app())
        db.create_all(app=db.get_app())
        click.echo('Initialized the database.')

    return app
