from flask_restx import Namespace
from flask import make_response, Response
from src.utils.base_resource_no_token_required import BaseResourceNoTokenRequired
from src.utils.http_status_code_enum import HttpStatusCodeEnum

api = Namespace('HealthCheck', description='Health Check')


@api.route('')
class HealthCheck(BaseResourceNoTokenRequired):
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def get(self) -> Response:
        return make_response({'ok': True}, HttpStatusCodeEnum.OK.value)
