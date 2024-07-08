from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class PoolConnectionFactory:

    def __init__(self, pool_size: int = 5, max_overflow: int = 10, pool_timeout: int = 30, pool_recycle: int = 1800):
        """
        Initialize the connection pooling configuration
        :param pool_size: Maximum number of connections in the pool
        :param max_overflow: Maximum number of connections that can be created if pool is full
        :param pool_timeout: Time in seconds to wait before throwing an exception if no connection is available
        :param pool_recycle: Time in seconds to recycle (close and reopen) inactive connections
        """
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_timeout = pool_timeout
        self.pool_recycle = pool_recycle

    def initialize(self, connection_string: str) -> scoped_session:
        """
        Initialize the connection pool
        :param connection_string: Database connection string
        :return: Scoped session
        """
        engine = create_engine(
            connection_string,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_timeout=self.pool_timeout,
            pool_recycle=self.pool_recycle
        )

        session = scoped_session(sessionmaker(autocommit=False,
                                              autoflush=False,
                                              bind=engine))
        return session
