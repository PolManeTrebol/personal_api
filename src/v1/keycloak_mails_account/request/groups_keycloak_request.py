from flask import current_app
from requests import Response, get


class GroupsKeycloakRequest:
    def get(self, token: str) -> list[dict[str, type]]:
        try:
            base_url: str = current_app.config['KEYCLOAK_BASE_URL']
            url: str = f"{base_url}/admin/realms/trebol/groups"
            headers: dict = {'Authorization': f'Berer {token}'}
            response: Response = get(url=url, headers=headers, verify=False)
            response.raise_for_status()
            groups_fetched: list[dict[str, type]] = response.json()

            return groups_fetched
        except Exception:
            raise Exception('Error al obtener los usuarios de Keycloak')
