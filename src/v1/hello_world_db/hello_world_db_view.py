from flask_restx import Namespace, reqparse
from flask import make_response, Response
from injector import inject

from src.connection.connection import Connection
from src.model.market.subsystem import Subsystem
from src.model.market.tariff import Tariff
from src.utils.base_resource import BaseResource
from src.utils.endpoint_error import EndpointError
from src.utils.http_status_code_enum import HttpStatusCodeEnum
from src.utils.role_enums import RolesEnum
from src.decorators.check_permission import check_permission
from src.v1.hello_world_db.hello_world_db_repository import HelloWorldDbRepository

api = Namespace('HelloWorldDb', description='Hello World db Description')

parser = reqparse.RequestParser()
# parser.add_argument('Authorization', type=str, location='headers', help='Bearer Token', required=True)
parser.add_argument('message', location='args', type=str, help='Message description', required=True)


@api.route('')
class HelloWorldDb(BaseResource):

    @inject
    def __init__(self, connection: Connection, **kwargs) -> None:  # type: ignore
        self.connection = connection
        super().__init__(**kwargs)

    @api.expect(parser)
    @check_permission(RolesEnum.READ_ONLY.value)
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def get(self) -> Response:
        args = parser.parse_args()

        # Data
        subsystem_1: Subsystem = Subsystem(idsubsystem=1, subsystem='subsystem_1')
        subsystem_2: Subsystem = Subsystem(idsubsystem=2, subsystem='subsystem_2')
        tariff_1: Tariff = Tariff(idtariff=1, tariff='tariff_1')
        tariff_2: Tariff = Tariff(idtariff=2, tariff='tariff_2')

        subsystem_list: list[Subsystem] = [subsystem_1, subsystem_2]
        tariff_list: list[Tariff] = [tariff_1, tariff_2]

        # Operation
        repository: HelloWorldDbRepository = HelloWorldDbRepository(session=self.connection.session_pool)

        repository.upsert_in_transaction(subsystem_list=subsystem_list,
                                         tariff_list=tariff_list)
        result: tuple[list[Subsystem], list[Tariff]] = repository.select(args=args)
        repository.delete_in_transaction(args=args)

        # Mapping
        result_dict = {'subsystem_list': [{"subsystem": subsystem.subsystem,
                                           "idsubsystem": subsystem.idsubsystem} for subsystem in result[0]],
                       'tariff_list': [{"tariff": tariff.tariff,
                                        "idtariff": tariff.idtariff} for tariff in result[1]]}

        try:
            return make_response({'ok': True, 'result': result_dict}, HttpStatusCodeEnum.OK.value)
        # pylint: disable=duplicate-code
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
        # pylint: enable=duplicate-code
