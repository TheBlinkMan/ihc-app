import os
from app import create_app, db
from app.models import User, Role, Image, Message, VirtualLearningEnvironment
from flask import request, abort
import click
from flask_migrate import Migrate, upgrade

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.before_request
def only_json():
    if request.method in ['POST', 'PUT'] and not request.is_json:
        abort(400)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app,
            db=db,
            User=User,
            Role=Role,
            Image=Image,
            Message=Message,
            VirtualLearningEnvironment=VirtualLearningEnvironment)

@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Enable code coverage')
def test(coverage):
    """ Run unit tests """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def deploy():
    """ Run deployment tasks """
    upgrade()

    Role.insert_roles()
