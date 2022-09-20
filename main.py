'''
    main
'''

from dotenv import load_dotenv
from flask import Flask

from auth import auth_blueprint
from car import car_blueprint
from database.database import db_session, init_db
from parking_lot import parking_lot_blueprint

# load env
load_dotenv()

# create app
app = Flask(__name__)

# register blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(car_blueprint)
app.register_blueprint(parking_lot_blueprint)

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
