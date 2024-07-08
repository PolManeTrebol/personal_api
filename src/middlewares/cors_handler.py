import os
from flask import request
from src.constants.allowed_domains import ALLOWED_DOMAINS
from typing import Any


class CorsHandler:
    def add_cors_headers(self, response_headers: Any) -> Any:
        response_headers.add("Access-Control-Allow-Headers", 'Content-Type, Authorization')
        response_headers.add("Access-Control-Allow-Methods", 'GET, POST, OPTIONS, PUT, DELETE, PATCH')
        response_headers.add("Access-Control-Allow-Credentials", 'true')

        if "Origin" in request.headers:
            origin = request.headers['Origin']
            if os.environ['ENV'] in ['production', 'test']:
                if origin in ALLOWED_DOMAINS:
                    response_headers.add("Access-Control-Allow-Origin", origin)

            if os.environ['ENV'] == 'development':
                response_headers.add("Access-Control-Allow-Origin", '*')

        return response_headers
