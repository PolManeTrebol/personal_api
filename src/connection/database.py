from flask_sqlalchemy import SQLAlchemy
from src.metaclass.singleton_meta import SingletonMeta


class Database(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.db = SQLAlchemy()
