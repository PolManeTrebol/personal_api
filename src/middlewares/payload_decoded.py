class PayloadDecoded:
    def __init__(self, email: str, preferred_username: str, iduser: str, name: str) -> None:
        self.email = email
        self.preferred_username = preferred_username
        self.iduser = int(iduser)
        self.name = name
