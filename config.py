import datetime
import os
from typing import Dict


class BaseConfig:
    HOST = '127.0.0.1'
    PORT = 5000

    API_VERSION = 'v1'
    API_PREFIX = f'/api/{API_VERSION}'

    MESSAGES_ENDPOINT = f'{API_PREFIX}/messages'
    MESSAGE_ENDPOINT = f'{MESSAGES_ENDPOINT}/<message_id>'

    SIGNUP_ENDPOINT = f'{API_PREFIX}/auth/signup'
    SIGNIN_ENDPOINT = f'{API_PREFIX}/auth/signin'

    STATUS_ENDPOINT = f'{API_PREFIX}/status'

    JWT_SECRET_KEY = r'\xd1\xe7\xd3A8\x98%\xfb\x85\td\x12\xd2\x0f\t%~7-@\xda\xb0;\x16'
    TOKEN_TTL = datetime.timedelta(days=7)
    DB_TYPE = 'sqlite'
    DB_NAME = 'messageit.db'


class DevConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    DB_NAME = ':memory:'


_configs: Dict[str, type(BaseConfig)] = {
    'development': DevConfig
}


def _get_config(env_name='development') -> BaseConfig:
    env = os.environ.get('messageit_env', env_name)

    env_config = _configs.get(env)
    if not env_config:
        raise EnvironmentError('Could not find requested environment')

    return env_config


conf = _get_config()
