from werkzeug import Response, Request

from src.middlewares.class_authentication import ClassAuthentication, TEXT_PLAIN
from src.utils.http_status_code_enum import HttpStatusCodeEnum
from src.utils.opentelemetry_utils import add_opentelemetry_attributes
from typing import List


def handle_authentication(request: Request, authentication: ClassAuthentication,
                          url_token_not_required: List[str]) -> Response | None:
    try:
        add_opentelemetry_attributes(authentication)
    except ValueError as e:
        exception_thrown = Response(str(e), mimetype=TEXT_PLAIN, status=HttpStatusCodeEnum.UNAUTHORIZED.value)
        return Response.force_type(exception_thrown, request.environ)

    if not any(url in request.base_url for url in url_token_not_required):
        exception_thrown = authentication.check_authentication()
        if exception_thrown:
            return Response.force_type(exception_thrown, request.environ)  # Ensure correct type

    return None
