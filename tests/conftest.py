import os

import pytest


@pytest.fixture
def test_root_path():
    return os.path.dirname(__file__)
