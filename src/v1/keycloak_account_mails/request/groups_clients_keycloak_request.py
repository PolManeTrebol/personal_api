from flask import current_app
from requests import Response, get

from src.v1.keycloak_account_mails.proxies.keycloak_clients_group import KeycloakClientsGroup


class KeycloakGroupClientsRequest:

    def get(self, token: str) -> dict[str, type]:
        try:
            base_url: str = current_app.config['KEYCLOAK_BASE_URL']
            url: str = f"{base_url}/admin/realms/trebol/groups/{KeycloakClientsGroup.id}"
            headers: dict = {'Authorization': f'Bearer {token}'}

            response: Response = get(url=url, headers=headers, verify=False)
            response.raise_for_status()
            groups_fetched: dict[str, type] = response.json()

            return groups_fetched
        except Exception:
            raise Exception('Error al obtener los usuarios de Keycloak')
