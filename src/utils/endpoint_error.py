class EndpointError(Exception):
    def __init__(self, message: str, code: int) -> None:
        self.message: str = message
        self.code: int = code
