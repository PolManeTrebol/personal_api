from flask_restx import Namespace, reqparse
from flask import make_response, Response
from injector import inject

from src.utils.base_resource import BaseResource
from src.utils.endpoint_error import EndpointError
from src.utils.http_status_code_enum import HttpStatusCodeEnum
from src.utils.role_enums import RolesEnum
from src.decorators.check_permission import check_permission
from src.v1.keycloak_account_mails.domain.groups_by_account_extractor import GroupsByAccountExtractor
from src.v1.keycloak_account_mails.proxies.keycloak_proxy import KeycloakProxy
from src.v1.keycloak_account_mails.services.keycloak_account_mails_service import KeycloakGroupMailsService

api = Namespace('Keycloak group mails', description='Mails from a Keycloak group')

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str, location='headers', help='Bearer Token', required=True)
parser.add_argument('idaccount', location='args', type=int,
                    help='Id de la cuenta de la cual queremos obtener los mails', required=True)


@api.route('')
class KeycloakMailsGroupView(BaseResource):
    @inject
    def __init__(self, keycloak_proxy: KeycloakProxy, group_extractor: GroupsByAccountExtractor,
                 **kwargs) -> None:  # type: ignore
        self.keycloak_proxy = keycloak_proxy
        self.group_extractor = group_extractor
        super().__init__(**kwargs)

    @api.expect(parser)
    @check_permission(RolesEnum.WRITE_ONLY.value)
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def get(self) -> Response:
        args = parser.parse_args()
        try:
            service: KeycloakGroupMailsService = KeycloakGroupMailsService(keycloak_proxy=self.keycloak_proxy,
                                                                           group_extractor=self.group_extractor)

            mail_list: list = service.get_emails_from_idaccount(args.idaccount)

            return make_response(mail_list, HttpStatusCodeEnum.OK.value)
        except ValueError as ve:
            endpoint_error = EndpointError(f'Value error: {str(ve)}', HttpStatusCodeEnum.BAD_REQUEST.value)
            return make_response({'message': endpoint_error.message}, endpoint_error.code)
        except TypeError as te:
            endpoint_error = EndpointError(f'Type error: {str(te)}', HttpStatusCodeEnum.BAD_REQUEST.value)
            return make_response({'message': endpoint_error.message}, endpoint_error.code)
        except Exception as e:  # pylint: disable=broad-except
            endpoint_error = EndpointError(f'Internal Server Error: {str(e)}',
                                           HttpStatusCodeEnum.INTERNAL_SERVER_ERROR.value)
            return make_response({'message': endpoint_error.message}, endpoint_error.code)
