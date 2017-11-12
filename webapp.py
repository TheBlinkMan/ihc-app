import os
from app import create_app, db
from app.models import User, Role
from flask import request, abort
import click

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.before_request
def only_json():
    if request.method in ['POST', 'PUT'] and not request.is_json:
        abort(400)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Enable code coverage')
def test(coverage):
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
