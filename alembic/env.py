from __future__ import with_statement
import sys
import os
from logging.config import fileConfig
from unittest.mock import patch, Mock

from injector import Binder, Injector
from sqlalchemy import engine_from_config, text, Connection
from sqlalchemy import pool
from alembic import context

from src.connection.connection import Connection as MicroserviceConnection
from src.connection.vaultproxy import VaultProxy
from src.middlewares.authorization import Authorization
from src.middlewares.class_token import ClassToken
from src.middlewares.cors_handler import CorsHandler

from src.server import create_app
from src.connection.database import Database
from functools import wraps


# CONFIGURE THE DATABASE CONNECTION (1)
class AuthorizationTest(Authorization):
    def authorization(self) -> None:  # type: ignore
        return None


def mock_decorator(permission):  # type: ignore
    def decorator(f):  # type: ignore
        @wraps(f)
        def decorated_function(*args, **kwargs):  # type: ignore
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def configure(binder: Binder) -> None:
    class_token = Mock(spec=ClassToken)
    class_token.decode_token.return_value = None
    class_token.get_roles.return_value = []

    binder.bind(Authorization, AuthorizationTest(class_token))
    binder.bind(ClassToken, class_token)
    binder.bind(CorsHandler, CorsHandler())

    database = Database()
    vault = VaultProxy()
    pool_connection_factory = Mock(session=Mock())
    binder.bind(MicroserviceConnection, MicroserviceConnection(database=database, vault=vault,
                                                               pool_connection_factory=pool_connection_factory))


# GET ALL SCHEMAS FUNCTION(2)
def get_all_schemas(path: str) -> list[str]:
    schemas: list[str] = []

    for schema in os.listdir(path):
        if os.path.isdir(os.path.join(path, schema)):
            schemas.append(schema)

    return schemas


# CONFIGURE ENV AND PROJECT PATH (3)
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['ENV'] = 'development'
patch('src.decorators.check_permission.check_permission', mock_decorator).start()

# CREATE THE APP AND DATABASE FOR GENERATE METADATA FOR ALEMBIC (4)
injector = Injector([configure])
app = create_app(injector=injector)
db = Database().db

# CONFIGURE LOGGER
config = context.config
fileConfig(config.config_file_name)

# INJECT THE DATABASE CONNECTION AND GENERATE THE METADATA (4)
config.set_main_option('sqlalchemy.url', app.config['SQLALCHEMY_DATABASE_URI'])
target_metadata = db.metadata
schema_names_in_models: list[str] = get_all_schemas("src/model")


def include_name(name, type_, parent_names) -> bool:  # type: ignore
    if type_ == "schema":
        return name in schema_names_in_models
    return True


def create_schemas_if_not_exist(connection: Connection, schema_names: list[str]) -> None:
    for schema in schema_names:
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        include_name=include_name
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),  # type: ignore
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name
        )

        create_schemas_if_not_exist(connection, schema_names_in_models)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
