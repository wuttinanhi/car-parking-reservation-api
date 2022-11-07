"""
    main
"""

from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR

from flask import Flask, request
from flask_socketio import SocketIO, emit
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from auth import auth_blueprint
from car import car_blueprint
from chat.blueprint import blueprint as chat_blueprint
from chat.handler import ChatHandler
from database.database import db_session, init_db
from env_wrapper import load_env
from parking_lot import parking_lot_blueprint
from payment.blueprint import blueprint as payment_blueprint
from payment.service import PaymentService
from reservation.blueprint import blueprint as reservation_blueprint
from settings.blueprint import blueprint as settings_blueprint
from settings.service import SettingService
from user.blueprint import blueprint as user_blueprint

# load env
load_env()


# create app
app = Flask(
    __name__, static_folder="static", template_folder="static", static_url_path=""
)

# initialize database
init_db()

# if settings not exists then create new one
SettingService.setup_default_settings()

# setup payment
PaymentService.setup_payment()

# register blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(car_blueprint)
app.register_blueprint(parking_lot_blueprint)
app.register_blueprint(reservation_blueprint)
app.register_blueprint(settings_blueprint)
app.register_blueprint(payment_blueprint)
app.register_blueprint(chat_blueprint)
app.register_blueprint(user_blueprint)

# shutdown database session when request context end
@app.teardown_appcontext
def shutdown_session(__exception=None):
    db_session.remove()


# root path
@app.route("/")
def hello_world():
    return {"app": "car-parking-reservation-api", "version": "1.0"}


# global error handler
@app.errorhandler(Exception)
def error_handle(err: Exception):
    # web error
    if issubclass(type(err), ValidationError):
        err: ValidationError = err
        return err.messages_dict, BAD_REQUEST
    if issubclass(type(err), HTTPException):
        return {"error": str(err.description)}, err.code
    # internal error
    print(err)
    return {"error": "Internal server exception!"}, INTERNAL_SERVER_ERROR


# socketio setup
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, logger=False)

# register socketio chat handler
socketio.on_namespace(ChatHandler())

# socketio error handler
@socketio.on_error()
def on_error(err: Exception):
    emit("exception", {"exception": str(err)}, to=request.sid)


# if __name__ == "__main__":
#     print("===== START =====")
#     socketio.run(app)
