import json
from io import BytesIO
from unittest.mock import patch
from urllib.error import HTTPError, URLError

import pytest

from scanner.main import (
    load_config,
    check_api_connection,
    check_user_authentication,
    check_order_access,
    check_function_access,
)


def test_load_config(tmp_path):
    config_file = tmp_path / "config.json"
    expected = {"base_url": "http://localhost:8000"}

    config_file.write_text(
        json.dumps(expected),
        encoding="utf-8",
    )

    with patch("scanner.main.CONFIG_PATH", config_file):
        assert load_config() == expected


def test_api_connection_success():
    with patch("scanner.main.urlopen") as mock:
        response = mock.return_value.__enter__.return_value
        response.status = 200

        assert check_api_connection(
            "http://localhost:8000"
        ) == 200


def test_api_connection_http_error():
    error = HTTPError(
        "http://localhost:8000/api/user",
        401, "Unauthorized", None, None
    )

    with patch("scanner.main.urlopen", side_effect=error):
        assert check_api_connection(
            "http://localhost:8000"
        ) == 401


def test_api_connection_failure():
    with patch(
        "scanner.main.urlopen",
        side_effect=URLError("Connection refused"),
    ):
        assert check_api_connection(
            "http://localhost:8000"
        ) is None


@pytest.mark.parametrize("function,args", [
    (check_user_authentication, ("mock-token",)),
    (check_order_access, ("/api/orders/{id}", 1, "mock-token")),
    (check_function_access, ("/api/admin/orders", "mock-token")),
])
def test_successful_response(function, args):
    response = BytesIO(b'{"user_id": 1}')
    response.status = 200

    with patch("scanner.main.urlopen") as mock:
        mock.return_value.__enter__.return_value = response

        result = function("http://localhost:8000", *args)

        request = mock.call_args.args[0]

        assert request.get_header("Authorization") == "Bearer mock-token"
        assert request.get_method() == "GET"

    assert result == (200, {"user_id": 1})


@pytest.mark.parametrize("function,args", [
    (check_user_authentication, ("mock-token",)),
    (check_order_access, ("/api/orders/{id}", 1, "mock-token")),
    (check_function_access, ("/api/admin/orders", "mock-token")),
])
def test_http_error(function, args):
    error = HTTPError(
        "http://localhost:8000",
        403, "Forbidden", None, None
    )

    with patch("scanner.main.urlopen", side_effect=error):
        result = function("http://localhost:8000", *args)

    assert result == (403, {})


def test_authentication_connection_failure():
    with patch(
        "scanner.main.urlopen",
        side_effect=URLError("Connection refused"),
    ):
        result = check_user_authentication(
            "http://localhost:8000",
            "mock-token",
        )

    assert result == (None, {})