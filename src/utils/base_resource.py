from flask_restx import Resource
from typing import List, Any


class BaseResource(Resource):
    method_decorators: List[Any] = []

    def dispatch_request(self, *args: Any, **kwargs: Any) -> Any:
        # Check if check_permission decorator is applied
        for method_name in ['get', 'post', 'put', 'delete', 'patch']:
            method = getattr(self, method_name, None)
            has_permission_decorator = self.check_permission_decorator_presence(method)
            if method and not has_permission_decorator:
                raise TypeError(f"The method {method_name} of {self.__class__.__name__} "
                                f"must be decorated with check_permission")
        return super().dispatch_request(*args, **kwargs)

    def check_permission_decorator_presence(self, method: Any) -> bool:
        # Check if the method has the _is_check_permission_decorated attribute set by the decorator
        return getattr(method, 'is_check_permission_decorated', False)
