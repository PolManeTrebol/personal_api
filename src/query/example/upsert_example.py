from sqlalchemy.orm import scoped_session

from src.connection.pool_connection_factory import PoolConnectionFactory
from src.model.market.subsystem import Subsystem
from src.query.upsert.upsert_postgresql import UpsertPostgresSQL


class UpsertExample:

    def __init__(self) -> None:
        subsystem_1: Subsystem = Subsystem(idsubsystem=1, subsystem='subsystem_1')
        subsystem_2: Subsystem = Subsystem(idsubsystem=2, subsystem='subsystem_2')

        self.subsystem_list: list[Subsystem] = [subsystem_1, subsystem_2]

    def execute_upsert(self) -> None:
        # Replace this for global pooling connection
        postgresql: str = 'postgresql://root:1234@localhost:32768/postgres'
        pool_connection_factory: PoolConnectionFactory = PoolConnectionFactory()
        session: scoped_session = pool_connection_factory.initialize(postgresql)
        # Replace this for global pooling connection

        primary_keys_list: list[str] = [Subsystem.idsubsystem.name]

        upsert = UpsertPostgresSQL(data=self.subsystem_list,  # type: ignore
                                   session=session,
                                   orm_table=Subsystem,
                                   primary_keys=primary_keys_list,
                                   remove_none_attributes=True)
        upsert.bulk_upsert()
