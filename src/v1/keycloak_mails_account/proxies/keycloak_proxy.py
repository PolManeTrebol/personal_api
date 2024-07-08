from datetime import datetime, timedelta
from typing import Dict, List, Any
import re
import requests
import urllib3

from src.v1.keycloak_mails_account.request.groups_clients_keycloak_request import GroupsClientsKeycloakRequest
from src.v1.keycloak_mails_account.request.groups_keycloak_request import GroupsKeycloakRequest
from src.v1.keycloak_mails_account.request.keycloak_token_request import KeycloakTokenRequest


class KeycloakProxy:
    def __init__(self):
        self.__session = requests.Session()
        self.__session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        self.__token: str = ""
        self.__token_session: datetime | None = None
        self.account_ids = []

    def get_token(self) -> None:
        try:
            if not self.__token or not self.__token_session or datetime.now() >= self.__token_session - timedelta(
                    minutes=10):
                urllib3.disable_warnings()
                token_request: KeycloakTokenRequest = KeycloakTokenRequest()
                token_information_response: Dict[str, any] = token_request.get_token()
                self.__token = token_information_response.get('access_token', '')
                self.__session.headers.update({'Authorization': f"Bearer {self.__token}"})
                expires_in = token_information_response.get('expires_in', 3600)
                self.__token_session = datetime.now() + timedelta(seconds=expires_in)
        except Exception as e:
            self.close()
            raise Exception(f'Error al obtener el token de Keycloak, {e}')

    def __get_clients_group(self):
        self.get_token()
        group_query: GroupsKeycloakRequest = GroupsKeycloakRequest(self.__session)
        groups_keycloak_fetched: Dict[str, List[Dict[str, Any]]] = group_query.get()
        target_path = '/all/external/clients'
        target_name = 'clients'
        client_id = self.__find_id_by_path(groups_keycloak_fetched, target_path, target_name)

        self.close()
        return client_id

    def get_groups(self, idaccount):
        self.get_token()
        group_query: GroupsClientsKeycloakRequest = GroupsClientsKeycloakRequest(self.__session)
        groups_keycloak_fetched: Dict[str, List[Dict[str, Any]]] = group_query.get(self.__get_clients_group())

        # return groups_keycloak_fetched
        self.recurse_groups(groups_keycloak_fetched, idaccount)

        self.close()
        return self.account_ids

    def recurse_groups(self, group, id_account):
        # Verificar si 'clientRoles' existe y tiene 'portal' dentro
        if 'clientRoles' in group and 'portal' in group['clientRoles']:
            # Iterar sobre cada ruta del portal
             for path in group['clientRoles']['portal']:
                # Usar expresiones regulares para buscar coincidencias con el patrón específico
                match = re.match(f'/resources/accounts/{id_account}/', path)
                if match:
                    # Agregar el id de la cuenta a la lista si se encuentra una coincidencia
                    self.account_ids.append(group['id'])

        # Recursivamente buscar en los subgrupos si existen
        if 'subGroups' in group:
            for sub_group in group['subGroups']:
                self.recurse_groups(sub_group, id_account)


    def __find_id_by_path(self, data, target_path, target_name):
        for item in data:
            if item['path'] == target_path and item['name'] == target_name:
                return item['id']
            # Si el elemento tiene subgrupos, aplicamos la recursividad
            if 'subGroups' in item:
                result = self.__find_id_by_path(item['subGroups'], target_path, target_name)
                if result:
                    return result
        return None  # Si no encontramos nada, retornamos None

    def close(self):
        self.__session.close()
