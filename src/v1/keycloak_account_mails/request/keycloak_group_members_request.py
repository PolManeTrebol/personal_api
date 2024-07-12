from flask import current_app
from requests import Response, get


class KeycloakGroupMembersRequest:
    def get(self, token: str, group_id: str) -> dict[str, type]:
        try:
            base_url: str = current_app.config['KEYCLOAK_BASE_URL']
            url: str = f"{base_url}/admin/realms/trebol/groups/{group_id}/members"
            headers: dict = {'Authorization': f'Bearer {token}'}

            response: Response = get(url=url, headers=headers, verify=False)
            response.raise_for_status()
            members: dict[str, type] = response.json()

            return members
        except Exception:
            raise Exception('Error al obtener los miembros del grupo de Keycloak')
