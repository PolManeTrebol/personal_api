from datetime import datetime, timedelta
from typing import Dict, List, Any
import re
import requests
import urllib3

from src.v1.keycloak_mails_account.request.groups_clients_keycloak_request import GroupsClientsKeycloakRequest
from src.v1.keycloak_mails_account.request.groups_keycloak_request import GroupsKeycloakRequest
from src.v1.keycloak_mails_account.request.keycloak_token_request import KeycloakTokenRequest


class KeycloakProxy:
    def get_token(self) -> str:
        token_request: KeycloakTokenRequest = KeycloakTokenRequest()
        token_information_response: Dict[str, any] = token_request.get_token()
        token = token_information_response.get('access_token', '')
        return token


    def get_subgroups_from_clients(self, token: str):
        group_query: GroupsClientsKeycloakRequest = GroupsClientsKeycloakRequest()
        groups_keycloak_fetched: list[dict[str, Any]] = group_query.get(token)
        return groups_keycloak_fetched
