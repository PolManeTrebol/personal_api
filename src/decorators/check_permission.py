from functools import wraps
from typing import Any, Callable, TypeVar, cast
from flask import make_response, request
from jwt import DecodeError, ExpiredSignatureError

from src.middlewares.class_token import ClassToken
from src.utils.http_status_code_enum import HttpStatusCodeEnum

F = TypeVar('F', bound=Callable[..., Any])


def check_permission(permission: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            token = request.headers.get('Authorization')
            if not token:
                return make_response(
                    {'error': 'No token provided',
                     'message': 'Authorization token is missing',
                     'status_code': HttpStatusCodeEnum.UNAUTHORIZED.value},
                    HttpStatusCodeEnum.UNAUTHORIZED.value)

            class_token = ClassToken()
            try:
                class_token.decode_token(token)
                valid = class_token.is_valid()
                if not valid or isinstance(valid,str):
                    message = f"Invalid token: {valid}" if isinstance(valid, str) else "Invalid token"
                    raise ValueError(message)
                resources = class_token.get_roles()
            except (DecodeError, ExpiredSignatureError, ValueError, KeyError) as e:
                return make_response(
                    {'error': 'Token error',
                     'message': str(e),
                     'status_code': HttpStatusCodeEnum.UNAUTHORIZED.value},
                    HttpStatusCodeEnum.UNAUTHORIZED.value)
            except Exception:  # pylint: disable=broad-except
                return make_response(
                    {'error': 'Unexpected error',
                     'message': 'An unexpected error occurred',
                     'status_code': HttpStatusCodeEnum.UNAUTHORIZED.value},
                    HttpStatusCodeEnum.UNAUTHORIZED.value)

            if permission in resources:
                return func(*args, **kwargs)

            return make_response(
                {'error': 'Permisos insuficientes',
                 'message': 'No tienes permiso para acceder a este recurso',
                 'status_code': HttpStatusCodeEnum.UNAUTHORIZED.value},
                HttpStatusCodeEnum.UNAUTHORIZED.value)

        wrapper.is_check_permission_decorated = True  # type: ignore[attr-defined]
        return cast(F, wrapper)

    return decorator
