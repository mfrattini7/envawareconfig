import os
from unittest import mock

import pytest

from envawareconfig import load_config, MissingEnvVarError

TEST_CONFIG_FILE = "tests/test-config.yaml"


@pytest.fixture()
def expected_default():
    yield {
        "database": {
            "name": "my-database",
            "user": "admin",
            "password": "my-password",
            "port": 1234,
            "maxConnections": 100
        }
    }


def test_missing_db_password():
    with pytest.raises(MissingEnvVarError) as e:
        load_config(TEST_CONFIG_FILE)
    assert str(e.value) == "No value found for: DB_PASSWORD"


@mock.patch.dict(os.environ, {"DB_PASSWORD": "my-password"}, clear=True)
def test_missing_db_max_connections():
    with pytest.raises(MissingEnvVarError) as e:
        load_config(TEST_CONFIG_FILE)
    assert str(e.value) == "No value found for: DB_MAX_CONNECTIONS"


@mock.patch.dict(os.environ, {"DB_PASSWORD": "my-password", "DB_MAX_CONNECTIONS": "100"}, clear=True)
def test_defaults(expected_default):
    assert load_config(TEST_CONFIG_FILE) == expected_default


@mock.patch.dict(
    os.environ,
    {"DB_USER": "my-user", "DB_PASSWORD": "my-password", "DB_PORT": "5432", "DB_MAX_CONNECTIONS": "100"},
    clear=True
)
def test_defaults_overridden(expected_default):
    actual = load_config(TEST_CONFIG_FILE)
    expected = expected_default
    expected["database"]["user"] = "my-user"
    expected["database"]["port"] = 5432
    assert actual == expected


@mock.patch.dict(
    os.environ,
    {"DB_PASSWORD": "my-password", "DB_MAX_CONNECTIONS": "100", "SOMETHING": "something"},
    clear=True
)
def test_extra_variables_do_no_harm(expected_default):
    assert load_config(TEST_CONFIG_FILE) == expected_default
