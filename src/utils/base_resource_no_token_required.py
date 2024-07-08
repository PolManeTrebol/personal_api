from typing import Any

from src.utils.base_resource import BaseResource


class BaseResourceNoTokenRequired(BaseResource):
    def check_permission_decorator_presence(self, method: Any) -> bool:
        if method:
            return True
        return False
