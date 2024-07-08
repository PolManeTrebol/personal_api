class Config:
    DEBUG = False
    TESTING = False
    CLIENT_ID = "75c3c41a-b2f3-4250-b77a-26172141aeb2"
    SCOPE = ["User.ReadBasic.All"]
    SESSION_TYPE = "filesystem"
    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    ROUTE = '/portal'
    FLASK_PORT = 5001
    TMP_PATH = '/app/main/tmp/'
    MAIN_PATH = '/app/main/'


class DevelopmentConfig(Config):
    # pylint: disable=too-many-instance-attributes
    def __init__(self, connection_string: str | None = None):
        self.FLASK_ENV: str = 'development'
        self.SESSION_COOKIE_SECURE: bool = False
        self.ROUTE: str = '/portal-test'
        self.FLASK_PORT: int = 5001
        self.TMP_PATH: str = './tmp/'
        self.MAIN_PATH: str = '../'
        self.SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
        self.SQLALCHEMY_DATABASE_URI: str | None = connection_string
    # pylint: enable=too-many-instance-attributes


class TestConfig(Config):
    FLASK_ENV = 'development'
    TESTING = True
    SESSION_COOKIE_SECURE = False
    ROUTE = '/portal-test'
    FLASK_PORT = 5001
    TMP_PATH = '/app/main/tmp/'
    MAIN_PATH = '/app/main/'
