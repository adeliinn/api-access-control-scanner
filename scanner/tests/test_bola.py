from unittest.mock import patch

import pytest

from scanner.main import run_bola_test


@pytest.fixture
def config():
    return {
        "users": {
            "alice": {
                "role": "user",
                "user_id": 1,
                "token_env": "ALICE_TOKEN",
            },
            "bob": {
                "role": "user",
                "user_id": 2,
                "token_env": "BOB_TOKEN",
            },
            "admin": {
                "role": "admin",
                "user_id": 3,
                "token_env": "ADMIN_TOKEN",
            },
        },
        "resources": {
            "alice_order_id": 1,
            "bob_order_id": 3,
        },
        "endpoints": {
            "secure": "/api/orders/{id}",
        },
    }


@pytest.mark.parametrize(
    "actor,owner,status,data,expected_status,expected_result",
    [
        ("alice", "alice", 200, {"user_id": 1}, 200, "PASS"),
        ("alice", "bob", 403, {}, 403, "PASS"),
        ("admin", "bob", 200, {"user_id": 2}, 200, "PASS"),
        ("alice", "bob", 200, {"user_id": 2}, 403, "VULNERABLE"),
        ("bob", "alice", 200, {"user_id": 1}, 403, "VULNERABLE"),
        ("alice", "alice", 500, {}, 200, "FAIL"),
        ("alice", "alice", 200, {"user_id": 2}, 200, "FAIL"),
        ("alice", "alice", 200, [], 200, "FAIL"),
        ("alice", "alice", None, {}, 200, "FAIL"),
        ("unauthenticated", "alice", 401, {}, 401, "PASS"),
        ("invalid_token", "bob", 401, {}, 401, "PASS"),
    ],
)
def test_bola_classification(
    config,
    actor,
    owner,
    status,
    data,
    expected_status,
    expected_result,
):
    test_case = {
        "id": "UNIT-BOLA",
        "actor": actor,
        "resource_owner": owner,
        "endpoint": "secure",
        "expected_status": expected_status,
    }

    with patch("scanner.main.os.getenv", return_value="mock-token"):
        with patch(
            "scanner.main.check_order_access",
            return_value=(status, data),
        ):
            result = run_bola_test(
                "http://localhost:8000",
                config,
                test_case,
            )

    assert result["result"] == expected_result
    assert result["actual_status"] == status




def test_bola_missing_token(config):
    test_case = {
        "id": "UNIT-BOLA-MISSING-TOKEN",
        "actor": "alice",
        "resource_owner": "bob",
        "endpoint": "secure",
        "expected_status": 403,
    }

    with patch("scanner.main.os.getenv", return_value=None):
        with patch("scanner.main.check_order_access") as mock:
            result = run_bola_test(
                "http://localhost:8000",
                config,
                test_case,
            )

            mock.assert_not_called()

    assert result["result"] == "FAIL"
    assert result["actual_status"] is None
    assert result["order_id"] is None
    assert result["error"] == "Authentication token is missing"