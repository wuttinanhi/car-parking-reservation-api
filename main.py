'''
    main
'''


from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR

from flask import Flask
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from auth import auth_blueprint
from car import car_blueprint
from database.database import db_session, init_db
from env_wrapper import load_env
from parking_lot import parking_lot_blueprint
from reservation.blueprint import blueprint as reservation_blueprint
from settings.blueprint import blueprint as settings_blueprint

# load env
load_env()


# create app
app = Flask(__name__)

# register blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(car_blueprint)
app.register_blueprint(parking_lot_blueprint)
app.register_blueprint(reservation_blueprint)
app.register_blueprint(settings_blueprint)

# shutdown database session when request context end


@app.teardown_appcontext
def shutdown_session(__exception=None):
    db_session.remove()


# initialize database
init_db()


# root path
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.errorhandler(Exception)
def error_handle(err: Exception):
    # web error
    if issubclass(type(err), ValidationError):
        return str(err), BAD_REQUEST
    if issubclass(type(err), HTTPException):
        return {'error': err.description}, err.code
    # internal error
    print(err)
    return {'error': "Internal server exception!"}, INTERNAL_SERVER_ERROR
