from typing import List, Dict, Any

from flask import current_app
from requests import Session, Response


class GroupsKeycloakRequest:

    def __init__(self, proxy_session: Session):
        self.__proxy_session: Session = proxy_session

    def get(self) -> Dict[str, List[Dict[str, Any]]]:
        try:
            base_url: str = current_app.config['KEYCLOAK_BASE_URL']
            groups_keycloak: Dict[str, List[Dict[str, Any]]] = {}
            url: str = f"{base_url}/admin/realms/trebol/groups"
            response: Response = self.__proxy_session.get(url=url, verify=False)
            response.raise_for_status()
            groups_fetched: List[Dict[str, Any]] = response.json()

            return groups_fetched
        except Exception:
            self.__proxy_session.close()
            raise Exception('Error al obtener los usuarios de Keycloak')
