from unittest.mock import patch

import pytest

from scanner.main import run_bfla_test


@pytest.fixture
def config():
    return {
        "users": {
            "alice": {
                "role": "user",
                "token_env": "ALICE_TOKEN",
            },
            "bob": {
                "role": "user",
                "token_env": "BOB_TOKEN",
            },
            "admin": {
                "role": "admin",
                "token_env": "ADMIN_TOKEN",
            },
        },
        "endpoints": {
            "secure": "/api/admin/orders",
        },
    }


@pytest.mark.parametrize(
    "actor,status,expected_status,expected_result",
    [
        ("alice", 403, 403, "PASS"),
        ("bob", 403, 403, "PASS"),
        ("admin", 200, 200, "PASS"),
        ("alice", 200, 403, "VULNERABLE"),
        ("bob", 200, 403, "VULNERABLE"),
        ("unauthenticated", 401, 401, "PASS"),
        ("invalid_token", 401, 401, "PASS"),
        ("admin", 403, 200, "FAIL"),
        ("alice", 500, 403, "FAIL"),
        ("alice", None, 403, "FAIL"),
    ],
)
def test_bfla_classification(
    config,
    actor,
    status,
    expected_status,
    expected_result,
):
    test_case = {
        "id": "UNIT-BFLA",
        "actor": actor,
        "endpoint": "secure",
        "expected_status": expected_status,
    }

    with patch("scanner.main.os.getenv", return_value="mock-token"):
        with patch(
            "scanner.main.check_function_access",
            return_value=(status, {}),
        ):
            result = run_bfla_test(
                "http://localhost:8000",
                config,
                test_case,
            )

    assert result["result"] == expected_result
    assert result["actual_status"] == status


def test_bfla_missing_token(config):
    test_case = {
        "id": "UNIT-BFLA-MISSING-TOKEN",
        "actor": "alice",
        "endpoint": "secure",
        "expected_status": 403,
    }

    with patch("scanner.main.os.getenv", return_value=None):
        with patch("scanner.main.check_function_access") as mock:
            result = run_bfla_test(
                "http://localhost:8000",
                config,
                test_case,
            )

            mock.assert_not_called()

    assert result["result"] == "FAIL"
    assert result["actual_status"] is None
    assert result["error"] == "Authentication token is missing"