from injector import Injector, Binder, singleton
from flask import Flask, Response
from flask_injector import FlaskInjector
# from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware

from src.connection.connection import Connection
from src.connection.database import Database
from src.connection.pool_connection_factory import PoolConnectionFactory
from src.connection.vaultproxy import VaultProxy
from src.middlewares.authorization import Authorization
from src.middlewares.class_token import ClassToken
from src.middlewares.cors_handler import CorsHandler
from src.utils.environment_configuration import EnvironmentConfiguration
from src.v1.v1_blueprint import v1_blueprint
# from src.middlewares.opentelemetry_middleware import OpenTelemetryMiddleware
# from src.utils.opentelemetry_config import configure_opentelemetry
from flask_migrate import Migrate  # type: ignore


def configure(binder: Binder) -> None:
    class_token = ClassToken()
    binder.bind(Authorization, to=Authorization(class_token))
    binder.bind(CorsHandler, to=CorsHandler())
    binder.bind(ClassToken, to=ClassToken())
    binder.bind(Migrate, to=Migrate())

    binder.bind(Database, to=Database, scope=singleton)
    binder.bind(VaultProxy, to=VaultProxy, scope=singleton)
    binder.bind(PoolConnectionFactory, to=PoolConnectionFactory, scope=singleton)

    binder.bind(Connection, to=Connection, scope=singleton)


def create_app(injector: Injector) -> Flask:
    app = Flask(__name__)

    # app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)  # type: ignore

    connection = injector.get(Connection)
    migrate = injector.get(Migrate)
    authorization = injector.get(Authorization)
    cors_handler = injector.get(CorsHandler)

    EnvironmentConfiguration(app).initialize_config_from_env(connection_string=connection.connection_string)

    # Define request handling functions inside the create_app function
    def before_request() -> None:
        authorization.authorization()

    def after_request(response: Response) -> Response:
        cors_handler.add_cors_headers(response.headers)
        return response

    # Register functions with Flask's before_request and after_request hooks
    app.before_request(before_request)
    app.after_request(after_request)

    connection.db.init_app(app)
    migrate.init_app(app, connection.db)

    # Routes
    app.register_blueprint(v1_blueprint, url_prefix='/v1/api')

    FlaskInjector(app=app, injector=injector)

    # pylint: disable=import-outside-toplevel
    # pylint: disable=unused-import
    from src import model
    # pylint: enable=import-outside-toplevel
    # pylint: enable=unused-import

    return app
