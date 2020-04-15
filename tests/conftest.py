import os
import sys
import pytest
from pathlib import Path
from pytest_docker_fixtures import images

from mindreader.drivers import Database, MessageQueue


@pytest.fixture
def data_dir():
    return Path(__file__).parent / 'data'


@pytest.fixture(scope="session")
def database(request) -> Database:
    init_db_docker = 'docker run -d -p 51347:27017 --name mongotest152 mongo'
    stop_db_docker = 'docker stop mongotest152'
    remove_db_docker = 'docker rm mongotest152'

    os.system(init_db_docker)

    def fin():
        os.system(stop_db_docker)
        os.system(remove_db_docker)

    request.addfinalizer(fin)
    return Database('mongodb://localhost:51347')


@pytest.fixture(scope="session")
def mq(request) -> MessageQueue:
    init_db_docker = 'docker run -d -p 51348:5672 --name rabbittest152 rabbitmq'
    stop_db_docker = 'docker stop rabbittest152'
    remove_db_docker = 'docker rm rabbittest152'

    os.system(init_db_docker)

    def fin():
        os.system(stop_db_docker)
        os.system(remove_db_docker)

    request.addfinalizer(fin)
    return MessageQueue('rabbitmq://127.0.0.1:51348')


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
