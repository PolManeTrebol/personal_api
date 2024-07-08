from sqlalchemy.orm import scoped_session

from src.connection.pool_connection_factory import PoolConnectionFactory
from src.model.market.subsystem import Subsystem
from src.model.market.tariff import Tariff
from src.query.upsert.upsert_postgresql import UpsertPostgresSQL


class TransactionExample:

    def __init__(self) -> None:
        subsystem_1: Subsystem = Subsystem(idsubsystem=1, subsystem='subsystem_1')
        subsystem_2: Subsystem = Subsystem(idsubsystem=2, subsystem='subsystem_2')

        self.subsystem_list: list[Subsystem] = [subsystem_1, subsystem_2]

        tariff_1: Tariff = Tariff(idtariff=1, tariff='tariff_1')
        tariff_2: Tariff = Tariff(idtariff=2, tariff='tariff_2')

        self.tariff_list: list[Tariff] = [tariff_1, tariff_2]

    def execute_transaction(self) -> None:
        # Replace this for global pooling connection
        postgresql: str = 'postgresql://root:1234@localhost:32768/postgres'
        pool_connection_factory: PoolConnectionFactory = PoolConnectionFactory()
        session: scoped_session = pool_connection_factory.initialize(postgresql)
        # Replace this for global pooling connection

        subsystem_primary_keys_list: list[str] = [Subsystem.idsubsystem.name]
        subsystem_upsert = UpsertPostgresSQL(data=self.subsystem_list, session=session, orm_table=Subsystem,  # type: ignore
                                             primary_keys=subsystem_primary_keys_list, remove_none_attributes=True)

        tariff_primary_keys_list: list[str] = [Tariff.idtariff.name]
        tariff_upsert = UpsertPostgresSQL(data=self.tariff_list, session=session, orm_table=Tariff,  # type: ignore
                                          primary_keys=tariff_primary_keys_list, remove_none_attributes=True)

        try:
            subsystem_upsert.bulk_upsert(do_commit=False)
            tariff_upsert.bulk_upsert(do_commit=False)

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
