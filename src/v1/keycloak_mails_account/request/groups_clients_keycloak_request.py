from typing import List, Dict, Any

from flask import current_app
from requests import Session, Response, get

from src.v1.keycloak_mails_account.proxies.keycloak_clients_group import KeycloakClientsGroup


class GroupsClientsKeycloakRequest:

    def get(self, token: str) -> list[dict[str, Any]]:
        try:
            base_url: str = current_app.config['KEYCLOAK_BASE_URL']
            url: str = f"{base_url}/admin/realms/trebol/groups/{KeycloakClientsGroup.id}"
            headers: dict = {'Authorization': f'Bearer {token}'}

            response: Response = get(url=url, headers=headers, verify=False)
            response.raise_for_status()
            groups_fetched: list[dict[str, Any]] = response.json()

            return groups_fetched
        except Exception:
            raise Exception('Error al obtener los usuarios de Keycloak')
