from flask_restx import Namespace, reqparse
from flask import make_response, Response
from src.utils.base_resource import BaseResource
from src.utils.endpoint_error import EndpointError
from src.utils.http_status_code_enum import HttpStatusCodeEnum
from src.utils.role_enums import RolesEnum
from src.decorators.check_permission import check_permission

api = Namespace('HelloWorld', description='Hello World Description')

parser = reqparse.RequestParser()
# parser.add_argument('Authorization', type=str, location='headers', help='Bearer Token', required=True)
parser.add_argument('message', location='args', type=str, help='Message description', required=True)


@api.route('')
class HelloWorld(BaseResource):
    @api.expect(parser)
    @check_permission(RolesEnum.READ_ONLY.value)
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def get(self) -> Response:
        args = parser.parse_args()
        try:
            return make_response({'ok': True, 'message': args.message}, HttpStatusCodeEnum.OK.value)
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
