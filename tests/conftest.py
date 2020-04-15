import os
import sys
import pytest
from pathlib import Path
from mindreader import drivers


@pytest.fixture
def data_dir():
    return Path(__file__).parent / 'data'


@pytest.fixture
def mock_database(monkeypatch):
    storage = {}

    class MockDatabase:
        def __init__(self, url):
            pass

        def insert_user(self, user):
            storage['user'] = user

        def insert_data(self, data):
            storage['data'] = data

    monkeypatch.setattr(drivers, 'Database', MockDatabase)
    return storage


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
