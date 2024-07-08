# utils/opentelemetry_utils.py

from opentelemetry import trace
from typing import Any

from src.middlewares.class_authentication import ClassAuthentication


def add_opentelemetry_attributes(authentication: ClassAuthentication) -> None:
    current_span = trace.get_current_span()
    decoded_token: dict[str, Any] = authentication.get_token().get_decoded_payload_dict() or {}
    current_span.set_attribute("authentication.iduser", decoded_token.get('iduser', 'undefined'))
    current_span.set_attribute("authentication.name",
                               decoded_token.get('name', 'undefined').encode(encoding='UTF-8', errors='strict'))
    current_span.set_attribute("authentication.email", decoded_token.get('email', 'undefined'))
    if 'email' in decoded_token:
        current_span.set_attribute("authentication.domain", decoded_token['email'].split('@')[1])
