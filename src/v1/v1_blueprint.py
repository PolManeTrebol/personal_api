from flask import Blueprint
from flask_restx import Api
from src.v1.hello_world.hello_world_view import api as hello_world_api
from src.v1.health_check.health_check_view import api as health_check_api
from src.v1.hello_world_db.hello_world_db_view import api as hello_world_db_api

v1_blueprint = Blueprint('v1_blueprint', __name__)

api = Api(v1_blueprint, doc='/doc', title='API plantilla', version='1.0.0', description='API plantilla')

api.add_namespace(hello_world_api, path='/hello-world')
api.add_namespace(health_check_api, path='/healthz')
api.add_namespace(hello_world_db_api, path='/hello-world-db')
