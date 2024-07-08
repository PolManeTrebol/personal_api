from typing import List, Dict, Any

from flask import current_app
from requests import Session, Response


class GroupsClientsKeycloakRequest:

    def __init__(self, proxy_session: Session):
        self.__proxy_session: Session = proxy_session

    def get(self, id_client:int) -> Dict[str, List[Dict[str, Any]]]:
        try:
            base_url: str = current_app.config['KEYCLOAK_BASE_URL']
            url: str = f"{base_url}/admin/realms/trebol/groups/{id_client}"
            response: Response = self.__proxy_session.get(url=url, verify=False)
            response.raise_for_status()
            groups_keycloak: List[Dict[str, Any]] = response.json()

            return groups_keycloak
        except Exception:
            self.__proxy_session.close()
            raise Exception('Error al obtener los usuarios de Keycloak')
