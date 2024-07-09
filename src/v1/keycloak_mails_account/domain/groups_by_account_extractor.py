import re
from typing import Any


class GroupsByAccountExtractor:

    def extract_groups_with_idaccount(self, group: dict[str, Any], idaccount:int) -> list[str]:
        # TODO
        # []
        # for
        # append self.__recurse_groups(group=group, id_account=idaccount)
        # return self.groups_ids


    def __recurse_groups(self, group: dict[str, Any], id_account):
        # Verificar si 'clientRoles' existe y tiene 'portal' dentro
        if 'clientRoles' in group and 'portal' in group['clientRoles']:
            # Iterar sobre cada ruta del portal
            for path in group['clientRoles']['portal']:
                # Usar expresiones regulares para buscar coincidencias con el patrón específico
                match = re.match(f'/resources/accounts/{id_account}/', path)
                if match:
                    # Agregar el id de la cuenta a la lista si se encuentra una coincidencia
                    self.groups_ids.append(group['id'])

        # Recursivamente buscar en los subgrupos si existen
        if 'subGroups' in group:

            for sub_group in group['subGroups']:
                self.__recurse_groups(sub_group, id_account)
