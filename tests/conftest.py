import os
import sys
import pytest
from pathlib import Path


@pytest.fixture
def json_snapshot_path():
    return Path(__file__).parent / 'data' / 'snapshot.json'


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
