from pylint.checkers import BaseChecker
from pylint.interfaces import HIGH


class NoResourceChecker(BaseChecker):
    __implements__ = BaseChecker

    name = 'no-resource-checker'
    priority = HIGH
    msgs = {
        'E9999': (
            'Class %s inherits from `Resource` instead of `BaseResource`',
            'no-resource-checker',
            'Ensure that classes inherit from `BaseResource` instead of `Resource`.'
        ),
    }
    options = ()

    def visit_classdef(self, node):
        if node.name == 'BaseResource':
            # Skip checking for the BaseResource class itself
            return
        for base in node.bases:
            if hasattr(base, 'name') and base.name == 'Resource':
                self.add_message('E9999', node=node, args=(node.name,))


def register(linter):
    linter.register_checker(NoResourceChecker(linter))
