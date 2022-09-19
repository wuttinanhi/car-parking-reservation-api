'''
    main
'''

from dotenv import load_dotenv
from flask import Flask

from auth import auth_blueprint
from car import car_blueprint
from database.database import db_session, init_db

load_dotenv()


app = Flask(__name__)


app.register_blueprint(auth_blueprint)
app.register_blueprint(car_blueprint)


@app.teardown_appcontext
def shutdown_session(__exception=None):
    db_session.remove()


init_db()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
