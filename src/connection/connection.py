from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy.orm import scoped_session

from src.connection.database import Database
from src.connection.pool_connection_factory import PoolConnectionFactory
from src.connection.vaultproxy import VaultProxy


@inject
class Connection:

    def __init__(self, database: Database, vault: VaultProxy, pool_connection_factory: PoolConnectionFactory):
        self.db: SQLAlchemy = database.db
        self.connection_string: str = vault.get_connection_string()
        self.session_pool: scoped_session = pool_connection_factory.initialize(self.connection_string)
