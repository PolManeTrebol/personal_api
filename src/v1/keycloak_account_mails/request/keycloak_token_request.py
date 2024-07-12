import requests
from flask import current_app
from requests import Response
from vault.credentials_manager import VaultCredentialsManager

from src.v1.keycloak_mails_account.proxies.keycloak_config import KeycloakConfig


class KeycloakTokenRequest:

    def get_token(self) -> dict[str, type]:
        try:
            base_url: str = current_app.config['KEYCLOAK_BASE_URL']
            vault = VaultCredentialsManager()
            username = vault.read_kv_secret(secret_path='production/portal_mail_credentials')['username']
            password = vault.read_kv_secret(secret_path='production/portal_mail_credentials')['password_keycloak']

            payload: dict[str, str] = {
                'username': username,
                'password': password,
                'client_id': KeycloakConfig.CLIENT_ID,
                'client_secret': KeycloakConfig.CLIENT_SECRET,
                'grant_type': KeycloakConfig.GRANT_TYPE
            }
            url: str = f"{base_url}/realms/trebol/protocol/openid-connect/token"
            response: Response = requests.post(url=url, data=payload, verify=False)
            response.raise_for_status()
            token_information_response: dict[str, type] = response.json()
            return token_information_response
        except Exception as e:
            raise Exception(f'Error al obtener el token de Keycloak: {str(e)}')
