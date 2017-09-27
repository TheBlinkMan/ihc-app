import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.route("/")
def hello():
    return "Hello World!"
