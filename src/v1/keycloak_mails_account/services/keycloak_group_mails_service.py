from src.v1.keycloak_mails_account.proxies.keycloak_proxy import KeycloakProxy


class KeycloakGroupMailsService:
    def get_emails_from_idaccount(self, idaccount:int)-> list:
        keycloak_proxy = KeycloakProxy()
        groups_info = keycloak_proxy.get_groups(idaccount)

        return groups_info