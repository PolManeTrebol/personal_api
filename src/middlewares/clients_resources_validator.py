from typing import List, Match
import re


class ClientsResourcesValidator:

    def __init__(self, resources: List[str], idaccount: int, idsocieties: List[int]) -> None:
        self.__resources = resources
        self.__idaccount = idaccount
        self.__idsocieties = idsocieties

    def check_resources(self) -> bool:
        if self._has_all_idaccounts() or self._has_all_idsocieties():
            return True

        is_available_idaccount = self._is_available_idaccount()
        idsocieties_available = self._get_idsocieties()
        return is_available_idaccount and idsocieties_available

    def _has_all_idaccounts(self) -> bool:
        resource_all_accounts = '/resources/accounts/*'
        return resource_all_accounts in self.__resources

    def _has_all_idsocieties(self) -> bool:
        resource_all_idsocieties = rf'^/resources/accounts/{self.__idaccount}/societies/\*'
        for resource in self.__resources:
            pattern_match = re.match(resource_all_idsocieties, resource)
            if pattern_match:
                return True
        return False

    def _is_available_idaccount(self) -> bool:
        resource_path = f'/resources/accounts/{self.__idaccount}'
        available_idaccount = any(item.startswith(resource_path) for item in self.__resources)
        return available_idaccount

    def _get_idsocieties(self) -> bool:
        my_list = []
        for resource in self.__resources:
            match = self._get_match_idsociety(resource=resource, idaccount=self.__idaccount)
            if match:
                idsociety = int(match.group(1))
                my_list.append(idsociety)
        my_list_unique = list(set(my_list))

        if not my_list_unique:
            raise PermissionError('User does not have permissions to access any society of this idaccount')

        idsocieties_available = all(x in my_list_unique for x in self.__idsocieties)
        return idsocieties_available

    def _get_match_idsociety(self, resource: str, idaccount: int) -> Match[str] | None:
        return re.search(rf'^/resources/accounts/{idaccount}/societies/([^/]+)$', resource)
