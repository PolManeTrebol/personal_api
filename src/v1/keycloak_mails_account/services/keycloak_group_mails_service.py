from flask import jsonify

from src.v1.keycloak_mails_account.domain.groups_by_account_extractor import GroupsByAccountExtractor
from src.v1.keycloak_mails_account.proxies.keycloak_proxy import KeycloakProxy


class KeycloakGroupMailsService:
    def __init__(self, keycloak_proxy: KeycloakProxy):
        self.keycloak_proxy = keycloak_proxy

    def get_emails_from_idaccount(self, idaccount: int) -> list[str]:
        keycloak_token: str = self.keycloak_proxy.get_token()

        keycloak_clients_groups = self.keycloak_proxy.get_subgroups_from_clients(token=keycloak_token)

        extractor = GroupsByAccountExtractor()
        groups_accounts_ids: list[str] = extractor.extract_groups_with_idaccount(clients_group=keycloak_clients_groups,
                                                                                 idaccount=idaccount)

        emails_list: set[str] = set()
        for group_account_id in groups_accounts_ids:
            current_account_emails = self.keycloak_proxy.get_emails_from_group(token=keycloak_token,
                                                                               group_id=group_account_id)
            emails_list.update(current_account_emails)

        return list(emails_list)
