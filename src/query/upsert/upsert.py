from abc import ABC, abstractmethod
from itertools import groupby
from types import MappingProxyType
from typing import TypeVar, Any

from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.orm import scoped_session

T = TypeVar('T')


class Upsert(ABC):
    def __init__(self, data: list[type], session: scoped_session, primary_keys: list[str], orm_table: type,
                 remove_none_attributes: bool = False, page_size: int = 0):
        self._data = data
        self._session = session
        self._primary_keys = primary_keys
        self._orm_table = orm_table
        self._remove_none_attributes = remove_none_attributes
        self._page_size = page_size
        self._name_to_get_excluded_rows: str | None = None

    def bulk_upsert(self, do_commit: bool = True) -> None:
        if self._page_size > 0:
            paginated_data: list[list[type]] = self._process_data_bulk_with_paginator()
            for page_num, page_data in enumerate(paginated_data):
                self._data = page_data
                self._process_data()
                if do_commit:
                    self._session.commit()
                print(f"Uploaded {len(page_data)} rows to {self._orm_table}, Page {page_num + 1}/{len(paginated_data)}")
                paginated_data[page_num] = []
        else:
            self._process_data()

    def _process_data_bulk_with_paginator(self) -> list[list[type]]:
        paginated_data: list[list[type]] = []
        for i in range(0, len(self._data), self._page_size):
            paginated_data.append(self._data[i:i + self._page_size])
        return paginated_data

    def _process_data(self) -> None:
        if self._remove_none_attributes:
            self._group_data_by_none_attributes()
            for data_with_same_attributes in self._data:
                self._bulk_upsert_data_with_same_attributes(data_with_same_attributes=data_with_same_attributes)  # type: ignore
        else:
            self._bulk_upsert_data_with_same_attributes(data_with_same_attributes=self._data)

    @abstractmethod
    def insert_if_possible(self, data_dict: list[dict[str, Any]]) -> Insert:
        pass

    @abstractmethod
    def update_on_duplicate_key(self, insert_statement: Insert, data_not_inserted_dict: dict[str, Any]) -> Insert:
        pass

    def _bulk_upsert_data_with_same_attributes(self, data_with_same_attributes: list[type]) -> None:
        data_dict: list[dict[str, Any]] = self._get_data_dict(data_with_same_attributes=data_with_same_attributes)
        data_dict = self._remove_none_attributes_if_required(list_of_dicts=data_dict)
        insert_statement: Insert = self.insert_if_possible(data_dict=data_dict)
        data_not_inserted_dict: dict[str, Any] = self._get_data_not_inserted_dict(dict_data=data_dict[0],
                                                                                    statement=insert_statement)
        insert_or_update_statement: Insert = self.update_on_duplicate_key(insert_statement=insert_statement,
                                                                          data_not_inserted_dict=data_not_inserted_dict)
        self._save(insert_or_update_statement=insert_or_update_statement)

    def _save(self, insert_or_update_statement: Insert) -> None:
        self._session.execute(insert_or_update_statement)
        self._session.commit()

    def _get_data_dict(self, data_with_same_attributes: list[type]) -> list[dict[str, Any]]:
        dict_data: dict[str, Any] = data_with_same_attributes[0].__dict__  # type: ignore
        dict_data = self._if_key_sa_instance_state_exist_delete(my_dict=dict_data)
        list_of_dict_data: list[dict[str, Any]] = []
        for data in data_with_same_attributes:
            dict_data_attributes: dict[str, Any] = self._get_dict_data_attributes(dict_data=dict_data, data=data)
            list_of_dict_data.append(dict_data_attributes)
        return list_of_dict_data

    def _get_dict_data_attributes(self, dict_data: dict[str, Any], data: type) -> dict[str, Any]:
        dict_data_attributes: dict[str, Any] = {}
        for key in dict_data.keys():
            attribute_value: type = getattr(data, key)
            dict_data_attributes[key] = attribute_value
        return dict_data_attributes

    def _remove_none_attributes_if_required(self, list_of_dicts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if self._remove_none_attributes:
            list_dict_no_nones = []
            for my_dict in list_of_dicts:
                dict_no_nones = self.remove_keys_if_none(my_dict)
                list_dict_no_nones.append(dict_no_nones)

            return list_dict_no_nones
        return list_of_dicts

    def _if_key_sa_instance_state_exist_delete(self, my_dict: dict[str, Any]) -> dict[str, Any]:
        key = '_sa_instance_state'
        if key in my_dict:
            my_dict.pop(key)
        return my_dict

    def _get_data_not_inserted_dict(self, dict_data: dict[str, Any], statement: Insert) -> dict[str, Any]:
        dict_excluded_attributes: dict[str, Any] = {}
        excluded = getattr(statement, self._name_to_get_excluded_rows)  # type: ignore
        for key in dict_data.keys():
            dict_excluded_attributes[key] = excluded[key]
        return dict_excluded_attributes

    def _group_data_by_none_attributes(self) -> None:
        data_concat_none_attributes: list[dict[str, Any]] = []
        dict_attributes: dict[str, Any] = self._data[0].__dict__  # type: ignore
        dict_attributes = self._if_key_sa_instance_state_exist_delete(my_dict=dict_attributes)
        for data in self._data:
            concat_of_none_attributes = ''
            for key in dict_attributes:
                if getattr(data, key) == None:
                    concat_of_none_attributes += '-' + key
            data_concat_none_attributes.append({'data': data, 'concat': concat_of_none_attributes})
        self._data = self._sort_and_group_by(data_concat_none_attributes=data_concat_none_attributes)  # type: ignore

    def _sort_and_group_by(self, data_concat_none_attributes: list[dict[str, Any]]) -> list[list[type]]:
        data_concat_none_attributes.sort(key=lambda x: x['concat'])
        data_concat_grouped = self.get_list_grouped_by(data_concat_none_attributes, lambda x: x['concat'])
        data_grouped_by_none_attributes = self._get_data_grouped(data_concat_grouped=data_concat_grouped)
        return data_grouped_by_none_attributes

    def _get_data_grouped(self, data_concat_grouped: list[list[dict[str, Any]]]) -> list[list[type]]:
        data_grouped: list[list[type]] = []
        for data_and_concat in data_concat_grouped:
            one_group_of_data: list[type] = self._get_all_group_of_data(data_and_concat=data_and_concat)
            data_grouped.append(one_group_of_data)
        return data_grouped

    def _get_all_group_of_data(self, data_and_concat: list[dict[str, Any]]) -> list[type]:
        group_of_data: list[type] = []
        for item in data_and_concat:
            group_of_data.append(item['data'])
        return group_of_data

    # before using this function you have to sort the attributes to group by
    @staticmethod
    def get_list_grouped_by(my_list: list[dict[str, Any]],
                            function_to_group_by: callable,  # type: ignore
                            sort: bool = False,
                            function_to_sort: callable = None) -> list[list[dict[str, Any]]]:  # type: ignore
        if sort:
            my_list.sort(key=function_to_sort)
        groups: list[list[dict[str, Any]]] = []
        for k, g in groupby(my_list, function_to_group_by):
            groups.append(list(g))
        return groups

    @staticmethod
    def remove_keys_if_none(my_dict: dict[str, Any]) -> dict[str, Any]:
        filtered = {k: v for k, v in my_dict.items() if v is not None}
        my_dict.clear()
        my_dict.update(filtered)
        return my_dict
