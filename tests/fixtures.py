from wsgi import application
from common.app_config import AppConfig
from common.config import config
from common.utils import *
from pytest import fixture
# python3 -m pytest -rsA tests/


@fixture
def test_api_client():
    application.testing = True
    return application.test_client()
