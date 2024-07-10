import re
from typing import Any


class GroupsByAccountExtractor:

    def extract_groups_with_idaccount(self, clients_group: dict[str, Any], idaccount: int) -> list[str]:
        groups_ids = []
        for group_account in clients_group['subGroups']:
            subgrpoups_ids = self._recurse_subgroups(group=group_account, id_account=idaccount)
            groups_ids.extend(subgrpoups_ids)
        return groups_ids

    def _recurse_subgroups(self, group: dict[str, Any], id_account) -> list[str]:
        groups_ids = []
        # Verificar si 'clientRoles' existe y tiene el cliente 'portal'
        if 'clientRoles' in group and 'portal' in group['clientRoles']:
            # Iterar sobre cada rol del portal
            for role in group['clientRoles']['portal']:
                if self.matching_roles(id_account, role):
                    groups_ids.append(group['id'])

        if 'subGroups' in group:
            for sub_group in group['subGroups']:
                groups_ids.extend(self._recurse_subgroups(sub_group, id_account))

        return groups_ids

    def matching_roles(self, id_account: int, role: str) -> bool:
        # Usar expresiones regulares para buscar coincidencias con el rol específico
        match = re.match(f'/resources/accounts/{id_account}', role)
        if match:
            return True

        return False
