from unittest.mock import patch
from json import JSONDecodeError
from urllib.error import URLError

import pytest

from scanner.main import (
    check_order_access,
    check_function_access,
)


@pytest.mark.parametrize("error", [
    JSONDecodeError("Invalid JSON", "", 0),
    TimeoutError("Request timeout"),
    URLError("Connection refused"),
])
def test_bola_error_handling(error):
    with patch("scanner.main.urlopen", side_effect=error):
        result = check_order_access(
            "http://localhost:8000",
            "/api/orders/{id}",
            1
        )

    assert result == (None, {})


@pytest.mark.parametrize("error", [
    JSONDecodeError("Invalid JSON", "", 0),
    TimeoutError("Request timeout"),
    URLError("Connection refused"),
])
def test_bfla_error_handling(error):
    with patch("scanner.main.urlopen", side_effect=error):
        result = check_function_access(
            "http://localhost:8000",
            "/api/admin/orders"
        )

    assert result == (None, {})