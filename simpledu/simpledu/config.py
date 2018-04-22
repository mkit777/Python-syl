# -*-coding:utf-8-*-

class BaseConfig:
    SECRET_KEY = 'makesure to set a very secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    INDEX_PER_PAGE = 9
    ADMIN_PER_PAGE = 15

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123@localhost:3306/simpledu?charset=utf8'


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


configs = {
    'development':DevelopmentConfig,
    'produciton':ProductionConfig,
    'testing':TestingConfig
}