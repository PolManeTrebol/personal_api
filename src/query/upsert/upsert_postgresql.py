from typing import Any

from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.orm import scoped_session

from src.query.upsert.upsert import Upsert, T


class UpsertPostgresSQL(Upsert):
    def __init__(self, data: list[type], session: scoped_session, primary_keys: list[str], orm_table: type,
                 remove_none_attributes: bool = False, page_size: int = 0):
        self._data = data
        self._session = session
        self._primary_keys = primary_keys
        self._orm_table = orm_table
        self._remove_none_attributes = remove_none_attributes
        self._page_size = page_size if page_size >= 0 else 0
        self._name_to_get_excluded_rows: str | None = 'excluded'

    def bulk_upsert(self, do_commit: bool = True) -> None:
        super().bulk_upsert(do_commit)

    def insert_if_possible(self, data_dict: list[dict[str, Any]]) -> Insert:
        insert_statement = postgresql.insert(self._orm_table).values(data_dict)
        return insert_statement

    def update_on_duplicate_key(self, insert_statement: Insert, data_not_inserted_dict: dict[str, Any]) -> Insert:
        insert_or_update_statement = insert_statement.on_conflict_do_update(index_elements=self._primary_keys,
                                                                            set_=data_not_inserted_dict)
        return insert_or_update_statement
