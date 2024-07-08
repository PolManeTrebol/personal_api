import json
from typing import List
from flask import request
from werkzeug import Response, Request
from src.middlewares.auth_utils import handle_authentication
from src.middlewares.class_authentication import ClassAuthentication
from src.middlewares.class_cors import ClassCors
from src.middlewares.class_token import ClassToken
from src.middlewares.clients_resources_validator import ClientsResourcesValidator
from src.middlewares.portal_test_validator import PortalTestValidator
from src.utils.http_status_code_enum import HttpStatusCodeEnum

URL_TOKEN_NOT_REQUIRED = ['/swaggerui/', '/v1/api/doc', '/v1/api/swagger.json', '/v1/api/healthz']


class Authorization:
    def __init__(self, class_token: ClassToken) -> None:
        self.class_token = class_token

    def authorization(self) -> Response:
        cors = ClassCors(request=request)
        exception_thrown = cors.check_cors()
        if exception_thrown is not None:
            return exception_thrown
        if request.path not in URL_TOKEN_NOT_REQUIRED:

            authentication = ClassAuthentication(request=request, class_token=self.class_token)

            exception_thrown = handle_authentication(request, authentication, URL_TOKEN_NOT_REQUIRED)
            if exception_thrown is not None:
                return exception_thrown

            exception_thrown = self._check_portal_permissions(auth_request=request, authentication=authentication)
            if exception_thrown is not None:
                return exception_thrown

        return Response('Authorization successful', status=HttpStatusCodeEnum.OK.value)

    def _check_portal_permissions(self, auth_request: Request, authentication: ClassAuthentication) -> Response:
        resource_and_features = self._get_resource_and_features(authentication=authentication)
        is_internal_permission = '/consulting/is_internal'

        if is_internal_permission in resource_and_features:
            return Response(status=HttpStatusCodeEnum.OK.value)

        origin = auth_request.headers.get('Origin')
        if origin and not self.valid_test_portal_access(origin=origin, resources=resource_and_features):
            return self._response_error(message="User doesn't have environment test permissions",
                                        http_status_code=HttpStatusCodeEnum.UNAUTHORIZED)

        idaccount = self._get_idaccount(auth_request)
        idsocieties = self._get_idsocieties(auth_request)

        valid_resources = ClientsResourcesValidator(resources=resource_and_features,
                                                    idaccount=idaccount,
                                                    idsocieties=idsocieties).check_resources()

        if not valid_resources:
            return self._response_error(message="User doesn't have any permissions",
                                        http_status_code=HttpStatusCodeEnum.UNAUTHORIZED)
        return Response(status=HttpStatusCodeEnum.OK.value)

    def valid_test_portal_access(self, origin: str, resources: List[str]) -> bool:
        portal_test_validator = PortalTestValidator()
        if (portal_test_validator.is_request_from_portal_test(origin) and
                not portal_test_validator.has_test_access(resources)):
            return False
        return True

    @staticmethod
    def _get_resource_and_features(authentication: ClassAuthentication) -> List[str]:
        token = authentication.get_token()
        resource_and_features = token.get_roles()
        return resource_and_features

    @staticmethod
    def _get_idaccount(auth_request: Request) -> int:
        if 'idaccount' not in auth_request.args:
            raise ValueError('Argument idaccount is required')

        return int(auth_request.args['idaccount'])

    @staticmethod
    def _get_idsocieties(auth_request: Request) -> List[int]:
        if 'idsocieties' not in auth_request.args:
            raise ValueError('Argument idsocieties is required')

        try:
            str_idsocieties = auth_request.args['idsocieties']
            idsocieties_splitted = str_idsocieties.split(',')
            idsocieties = [int(item) for item in idsocieties_splitted]
        except ValueError as exc:
            raise ValueError('Argument idsocieties is not a list of integers') from exc

        return idsocieties

    @staticmethod
    def _response_error(message: str, http_status_code: HttpStatusCodeEnum) -> Response:
        APPLICATION_JSON = 'application/json'
        data = {'message': message}
        response = json.dumps(data)
        return Response(response, mimetype=APPLICATION_JSON, status=http_status_code.value)
