import os

from werkzeug.wrappers import Request,Response
from src.constants.allowed_domains import ALLOWED_DOMAINS
from src.utils.http_status_code_enum import HttpStatusCodeEnum

TEXT_PLAIN = 'text/plain'


class ClassCors:
    def __init__(self, request: Request) -> None:
        self.request = request
        self.args = self.request.args

    def _check_origin_in_header(self) -> Response | None:
        if "Origin" not in self.request.headers and os.environ['ENV'] != 'development':
            message = 'Bad request: No "Origin" header provided.'
            return Response(message, mimetype=TEXT_PLAIN, status=HttpStatusCodeEnum.MISSING_ARGS.value)
        return None

    def _check_origin_allowed(self) -> Response | None:
        if os.environ['ENV'] == 'production' and self.request.headers['Origin'] not in ALLOWED_DOMAINS:
            message = 'Authorization failed: Origin ' + str(self.request.headers['Origin']) + ' not allowed.'
            return Response(message, mimetype=TEXT_PLAIN, status=HttpStatusCodeEnum.METHOD_NOT_ALLOWED.value)
        return None

    def _check_if_method_is_option(self) -> Response | None:
        if self.request.method == "OPTIONS":
            return Response(response=None, status=HttpStatusCodeEnum.OK.value)
        return None

    def _check_if_method_allowed(self) -> Response | None:
        ALLOWED_METHODS = ['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE', 'PATCH']

        if self.request.method not in ALLOWED_METHODS:
            message = 'Authorization failed: Method ' + str(self.request.method) + ' not allowed.'
            return Response(message, mimetype=TEXT_PLAIN, status=HttpStatusCodeEnum.METHOD_NOT_ALLOWED.value)
        return None

    def check_cors(self) -> Response | None:
        res = self._check_origin_in_header()
        if res:
            return res
        res = self._check_origin_allowed()
        if res:
            return res
        res = self._check_if_method_is_option()
        if res:
            return res
        res = self._check_if_method_allowed()
        if res:
            return res
        return None
