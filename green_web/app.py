import os
import logging
import logging.config
from flask import Flask, Blueprint
from flask_cors import CORS

from .config import env2config
from .api.restplus import api
from .api.data.endpoints.info import ns as data_info_ns
from .api.strain.endpoints.info import ns as strain_info_ns
from .api.bmus.endpoints.info import ns as bmus_info_ns

logger = logging.getLogger(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))


def configure_app(flask_app, environment='development'):
    """
    Configures the input app, based on deployment environment, by setting key-value pairs serving as settings.\n
    :param Flask flask_app: the app
    :param str environment:
    :type environment: one of {'default', 'development', 'testing', 'production'}
    """
    config_class_string = 'green_web.config.{}'.format(env2config[environment])
    flask_app.config.from_object(config_class_string)
    logger.info("Configuration class '{}' used for '{}' environment".format(config_class_string, environment))

    # flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    # flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS


def initialize_app(flask_app, environment):
    configure_app(flask_app, environment=environment)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(strain_info_ns)
    api.add_namespace(data_info_ns)
    api.add_namespace(bmus_info_ns)
    from .api.business import SM
    SM.datasets_dir = flask_app.config['DATASETS_DIR']
    SM.load_dataset('{}-clean.pk'.format(flask_app.config['DATASET_ID']))
    if not SM.dt.datapoints:
        SM.set_feature_vectors()
    flask_app.register_blueprint(blueprint)


# def init_app():
#     appl = Flask(__name__)
#     db.init_app(appl)
#     return appl


# app = init_app()
# p = '/data/projects/knowfly/green-machine/green-web/logging.conf'
# logging.config.fileConfig(p)
# logger = logging.getLogger(__name__)
# initialize_app(app)


def get_logger_n_app(environment='development'):
    app = Flask(__name__)
    initialize_app(app, environment)
    CORS(app)

    p = os.path.join(basedir, '../logging.conf')
    logging.config.fileConfig(p)
    logger = logging.getLogger(__name__)

    return logger, app
