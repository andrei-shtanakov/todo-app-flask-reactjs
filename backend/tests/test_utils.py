"""Pytest skeleton tests for `flaskr.utils`.

This file is intentionally minimal and should run without errors. Replace the
`pytest.skip` calls with real assertions as you implement the tests.
"""

import sys
from pathlib import Path

import pytest


# Ensure the `backend` directory (parent of this file's directory) is on sys.path
_BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))


from flaskr.utils import generate_password, check_password  # noqa: E402


class TestUtils:
    def test_generate_password_placeholder(self):
        # TODO: implement test logic for `generate_password`
        # Example idea: assert the returned value is a non-empty hash string
        pytest.skip("TODO: implement test for generate_password")

    def test_check_password_placeholder(self):
        # TODO: implement test logic for `check_password`
        # Example idea: generate a hash, then verify correct/incorrect passwords
        pytest.skip("TODO: implement test for check_password")


