from mindreader.client import client
import pytest


def test_path_not_exists():
    with pytest.raises(FileNotFoundError):
        client.upload_sample('127.0.0.1', 8000, path='')
