from mindreader import client
import pytest


def test_path_not_exists():
    with pytest.raises(FileNotFoundError):
        client.upload_sample('', '', '')


def test_sample_sent():
    pass