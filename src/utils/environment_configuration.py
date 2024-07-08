import os
from flask import Flask
from src.app_config import ProductionConfig, TestConfig, DevelopmentConfig, Config


class EnvironmentConfiguration:
    def __init__(self, app: Flask) -> None:
        self.app = app

    def initialize_config_from_env(self, connection_string: str | None = None) -> None:
        if 'ENV' not in os.environ:
            raise RuntimeError("No environment defined")
        if os.environ['ENV'] == 'production':
            self.__apply_config(self.app, ProductionConfig())
        elif os.environ['ENV'] == 'test':
            self.__apply_config(self.app, TestConfig())
        elif os.environ['ENV'] == 'pytest':
            self.__apply_config(self.app, TestConfig())
        elif os.environ['ENV'] == 'development':
            self.__apply_config(self.app, DevelopmentConfig(connection_string=connection_string))
        else:
            raise RuntimeError("Wrong environment defined")

    def __apply_config(self, app: Flask, config: Config) -> None:
        app.config.from_object(config)
