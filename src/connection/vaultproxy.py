

class VaultProxy:

    def get_connection_string(self) -> str:
        postgresql: str = 'postgresql://root:1234@localhost:32768/postgres'

        return postgresql
