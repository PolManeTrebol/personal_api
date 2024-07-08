from sqlalchemy.orm import scoped_session
from src.connection.pool_connection_factory import PoolConnectionFactory
from src.model.market.subsystem import Subsystem


class SelectExample:

    def __init__(self) -> None:
        pass

    def execute_select(self) -> list[Subsystem]:
        # Replace this for global pooling connection
        postgresql: str = 'postgresql://root:1234@localhost:32768/postgres'
        pool_connection_factory: PoolConnectionFactory = PoolConnectionFactory()
        session: scoped_session = pool_connection_factory.initialize(postgresql)
        # Replace this for global pooling connection

        try:
            query = session.query(Subsystem)
            result: list[Subsystem] = query.all()

            return result

        except Exception as e:
            raise e
