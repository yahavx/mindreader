import sys
import pytest
from pathlib import Path

sys.path.append(Path(__file__).parent.parent)


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
    from mindreader import drivers
    monkeypatch.setattr(drivers, 'Database', MockDatabase)
    return storage


