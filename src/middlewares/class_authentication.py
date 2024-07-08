from werkzeug.wrappers import Request, Response
from src.middlewares.class_token import ClassToken
from src.utils.endpoint_error import EndpointError
from src.utils.http_status_code_enum import HttpStatusCodeEnum

TEXT_PLAIN = 'text/plain'


class ClassAuthentication:
    def __init__(self, request: Request, class_token: ClassToken) -> None:
        self.request = request
        self.args = self.request.args
        self.token: ClassToken | None = None
        self.error: EndpointError | None = None
        self.email: str | None = None

        try:
            if self.request.headers.get('Authorization', None) is None:
                raise EndpointError('Authorization header not found.', HttpStatusCodeEnum.MISSING_ARGS.value)

            self.token = class_token
            self.token.decode_token(self.request.headers['Authorization'])

        except EndpointError as e:
            self.error = e

    def _check_token_valid(self) -> Response | None:
        if self.token is None or not self.token.is_valid() or isinstance(self.token, str):
            message = "Invalid token"
            if self.token is not None and isinstance(self.token.is_valid(), str):
                message = f"Invalid token: {self.token.is_valid()}"
            return Response(message, mimetype=TEXT_PLAIN, status=HttpStatusCodeEnum.INVALID_TOKEN.value)
        return None

    def _check_iss_tenant(self) -> Response | None:
        if self.token is None:
            message = 'Authorization failed: Token is missing.'
            return Response(message, mimetype=TEXT_PLAIN, status=HttpStatusCodeEnum.INVALID_TOKEN.value)

        payload_decoded_dict = self.token.get_decoded_payload_dict()
        if payload_decoded_dict is None:
            message = 'Authorization failed: Decoded payload is missing.'
            return Response(message, mimetype=TEXT_PLAIN, status=HttpStatusCodeEnum.INVALID_TOKEN.value)

        ISS_TENANT = [
            'https://portal.grupotrebolenergia.es/iss',
            'https://login.grupotrebolenergia.es/auth/realms/trebol'
        ]

        if 'iss' not in payload_decoded_dict or payload_decoded_dict['iss'] not in ISS_TENANT:
            message = 'Authorization failed: Token from outside our organization.'
            return Response(message, mimetype=TEXT_PLAIN, status=HttpStatusCodeEnum.INVALID_TOKEN.value)
        return None

    def check_authentication(self) -> Response:
        if self.error:
            return Response('Token contains an error: ' + self.error.message, mimetype=TEXT_PLAIN,
                            status=self.error.code)
        if (res := self._check_token_valid()) is not None:
            return res
        if (res := self._check_iss_tenant()) is not None:
            return res
        return Response('Authentication successful', mimetype=TEXT_PLAIN, status=HttpStatusCodeEnum.OK.value)

    def get_email(self) -> str | None:
        return self.email

    def get_token(self) -> ClassToken:
        if self.token is None:
            raise ValueError("Token is not set")
        return self.token
