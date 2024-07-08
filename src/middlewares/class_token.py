import base64
import json
from typing import Any, Dict, List
from jwcrypto import jwk, jwt
from jwcrypto.common import JWException
from jwcrypto.jwt import JWTExpired

from src.middlewares.jwks import JWKS
from src.middlewares.payload_decoded import PayloadDecoded


class ClassToken:
    def __init__(self) -> None:
        self.encoded_token: str | None = None
        self.header_decoded_dict: Dict[str, Any] | None = None
        self.payload_decoded_dict: Dict[str, Any] | None = None
        self.email: str | None = None
        self.iduser: str | None = None

    def decode_token(self, token: str) -> None:
        self.encoded_token = token.replace('Bearer ', '')
        header_decoded = base64.b64decode(self.encoded_token.split('.', maxsplit=1)[0] + "===")
        self.header_decoded_dict = json.loads(header_decoded.decode('utf8'))
        payload_decoded = base64.b64decode(self.encoded_token.split('.')[1] + "===")
        self.payload_decoded_dict = json.loads(payload_decoded.decode('utf8'))
        self.email = None

    def get_decoded_header(self) -> Dict[str, Any] | None:
        return self.header_decoded_dict

    def get_decoded_payload(self) -> PayloadDecoded:
        if self.payload_decoded_dict is None:
            raise ValueError("Payload is not decoded yet")
        payload_decoded = PayloadDecoded(
            iduser=self.payload_decoded_dict['iduser'],
            email=self.payload_decoded_dict['email'],
            name=self.payload_decoded_dict.get('name', ''),
            preferred_username=self.payload_decoded_dict['preferred_username']
        )
        return payload_decoded

    def get_decoded_payload_dict(self) -> Dict[str, Any] | None:
        return self.payload_decoded_dict

    def get_roles(self) -> List[str]:
        if self.payload_decoded_dict is None:
            raise ValueError("Payload is not decoded yet")
        return self.payload_decoded_dict['resource_access']['portal']['roles']

    def get_email(self) -> str:
        if self.payload_decoded_dict is None:
            raise ValueError("Payload is not decoded yet")
        if 'email' in self.payload_decoded_dict:
            self.email = self.payload_decoded_dict['email']
        elif 'preferred_username' in self.payload_decoded_dict:
            self.email = self.payload_decoded_dict["preferred_username"]
        if self.email is None:
            raise ValueError("Email not found in payload")
        return self.email

    def get_iduser(self) -> str:
        if self.payload_decoded_dict is None:
            raise ValueError("Payload is not decoded yet")
        if 'iduser' in self.payload_decoded_dict:
            self.iduser = self.payload_decoded_dict['iduser']
        if self.iduser is None:
            raise ValueError("ID user not found in payload")
        return self.iduser

    def is_valid(self) -> bool | str:
        try:
            token_has_content_after_third_dot = self._token_has_content_after_third_dot()
            kid = self._find_kid()
            key = jwk.JWK(**kid)
            et = self._get_et(key=key)
            return self._is_et_valid(et=et) and token_has_content_after_third_dot
        except JWTExpired:
            return "The token is expired"
        except (KeyError, ValueError, JWException):  # Catch specific exceptions
            return False

    def _token_has_content_after_third_dot(self) -> bool:
        if self.encoded_token is None:
            return False
        token_splitted = self.encoded_token.split('.')[2]
        return bool(token_splitted)

    def _find_kid(self) -> Dict[str, str]:
        if self.header_decoded_dict is None:
            raise ValueError("Header is not decoded yet")
        for keys in JWKS.values():
            for key in keys:
                if key['kid'] == self.header_decoded_dict['kid']:
                    return key
        return {}

    def _get_et(self, key: jwk.JWK) -> jwt.JWT:
        if self.encoded_token is None:
            raise ValueError("Encoded token is not set")
        return jwt.JWT(key=key, jwt=self.encoded_token)

    def _is_et_valid(self, et: jwt.JWT) -> bool:
        return et.validity >= 0
