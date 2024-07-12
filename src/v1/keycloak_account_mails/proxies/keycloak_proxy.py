import urllib3

from src.v1.keycloak_account_mails.request.groups_clients_keycloak_request import KeycloakGroupClientsRequest
from src.v1.keycloak_account_mails.request.keycloak_group_members_request import KeycloakGroupMembersRequest
from src.v1.keycloak_account_mails.request.keycloak_token_request import KeycloakTokenRequest


class KeycloakProxy:
    def get_token(self) -> str:
        urllib3.disable_warnings()
        token_request: KeycloakTokenRequest = KeycloakTokenRequest()
        token_information_response: dict[str, type] = token_request.get_token()
        token = token_information_response.get('access_token', '')
        return token

    def get_subgroups_from_clients(self, token: str):
        urllib3.disable_warnings()
        group_request: KeycloakGroupClientsRequest = KeycloakGroupClientsRequest()
        groups_keycloak_fetched: dict[str, type] = group_request.get(token)
        return groups_keycloak_fetched

    def get_emails_from_group(self, token: str, group_id: str) -> dict[str, type]:
        urllib3.disable_warnings()
        group_members_request: KeycloakGroupMembersRequest = KeycloakGroupMembersRequest()
        members: dict[str, type] = group_members_request.get(token=token, group_id=group_id)

        return members
