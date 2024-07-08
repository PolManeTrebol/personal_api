from flask_restx.reqparse import ParseResult
from sqlalchemy.orm import scoped_session

from src.model.market.subsystem import Subsystem
from src.model.market.tariff import Tariff
from src.query.upsert.upsert_postgresql import UpsertPostgresSQL


class HelloWorldDbRepository:

    def __init__(self, session: scoped_session) -> None:
        self.session = session

    def upsert_in_transaction(self, subsystem_list: list[Subsystem], tariff_list: list[Tariff]) -> None:

        subsystem_primary_keys_list = [Subsystem.idsubsystem.name]
        subsystem_upsert = UpsertPostgresSQL(data=subsystem_list, session=self.session, #  type: ignore
                                             orm_table=Subsystem,
                                             primary_keys=subsystem_primary_keys_list,
                                             remove_none_attributes=True)

        tariff_primary_keys_list = [Tariff.idtariff.name]
        tariff_upsert = UpsertPostgresSQL(data=tariff_list, session=self.session,  # type: ignore
                                          orm_table=Tariff, primary_keys=tariff_primary_keys_list,
                                          remove_none_attributes=True)

        try:
            subsystem_upsert.bulk_upsert(do_commit=False)
            tariff_upsert.bulk_upsert(do_commit=False)

            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def select(self, args: ParseResult) -> tuple[list[Subsystem], list[Tariff]]:
        try:
            query_subsystem = self.session.query(Subsystem)
            result_subsystem: list[Subsystem] = query_subsystem.all()

            query_tariff = self.session.query(Tariff)
            result_tariff: list[Tariff] = query_tariff.all()

            if args.message:
                pass #apply filter

            return result_subsystem, result_tariff

        except Exception as e:
            raise e

    def delete_in_transaction(self, args: ParseResult) -> None:
        try:
            self.session.query(Subsystem).delete()
            self.session.query(Tariff).delete()

            if args.message:
                pass #apply filter

            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
