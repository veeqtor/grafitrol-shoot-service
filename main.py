"""API Initialization Module"""
from dateutil import tz
from dotenv import load_dotenv
from flask import Flask, jsonify, Blueprint
from flask_restplus import Api
from flask_cors import CORS
from flask_migrate import Migrate

from config import app_config
from utils.error_handler import error_handlers

load_dotenv()

api_blueprint = Blueprint('api_bp', __name__, url_prefix='/api')
api = Api(api_blueprint)

endpoint = api.route

TIMEZONE = 'Africa/Lagos'
local_tz = tz.gettz(TIMEZONE)
utc = tz.UTC


def register_blueprints(application):
    """Registers all blueprints.

	Args:
		application (Obj): Flask Instance
	Returns:
		None
	"""

    application.register_blueprint(api_blueprint)


def create_app(current_env='development'):
    """
	Creates the flask application instance.
	Args:
		current_env (string): The current environment
	Returns:
		Object: Flask instance
	"""
    from database.config import db_session, init_db, engine

    app = Flask(__name__)
    origins = ['*']

    if current_env == 'development':
        import logging
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    CORS(app, origins=origins, supports_credentials=True)
    app.config.from_object(app_config[current_env])
    register_blueprints(app)
    error_handlers(app)

    init_db()
    Migrate(app, engine)

    import src.views

    @app.route('/', methods=['GET'])
    def health():
        """Index Route"""

        return jsonify(data={
            "status": 'success',
            "message": 'Grafitrol Shoots service is healthy'
        }, )

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Close the db session"""
        db_session.remove()

    return app
