'''
    main
'''

from flask import Flask

import blueprints.auth as auth
from services.database import db_session, init_db

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


app = Flask(__name__)


app.register_blueprint(auth.bp)


@app.teardown_appcontext
def shutdown_session(__exception=None):
    db_session.remove()


init_db()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
