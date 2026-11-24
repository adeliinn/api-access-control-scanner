import json
from unittest.mock import patch

import pytest

from scanner.main import main


@pytest.fixture
def config():
    return {
        "base_url": "http://localhost:8000",
        "users": {
            "alice": {
                "user_id": 1,
                "token_env": "ALICE_TOKEN",
                "role": "user",
            },
            "bob": {
                "user_id": 2,
                "token_env": "BOB_TOKEN",
                "role": "user",
            },
        },
        "resources": {
            "alice_order_id": 1,
            "bob_order_id": 3,
        },
        "endpoints": {
            "secure": "/api/orders/{id}",
            "vulnerable": "/api/vulnerable-orders/{id}",
        },
        "test_cases": [
            {"id": "TEST-01"},
            {"id": "TEST-02"},
            {"id": "TEST-03"},
        ],
    }


@pytest.mark.parametrize("status,message", [
    (None, "Could not connect to the API."),
    (500, "API returned HTTP 500."),
])
def test_main_connection_failure(config, status, message, capsys):
    with patch("scanner.main.load_config", return_value=config):
        with patch(
            "scanner.main.check_api_connection",
            return_value=status,
        ):
            with patch("scanner.main.run_bola_test") as mock:
                main()
                mock.assert_not_called()

    assert message in capsys.readouterr().out


def test_main_reports(config, tmp_path, capsys):
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    bfla_config = {
        "base_url": "http://localhost:8000",
        "test_cases": [
            {"id": "BFLA-01"},
            {"id": "BFLA-02"},
            {"id": "BFLA-03"},
        ],
    }

    config_path = config_dir / "bfla-test-config.json"
    config_path.write_text(
        json.dumps(bfla_config),
        encoding="utf-8",
    )

    bola_results = [
        {"test_id": "TEST-01", "result": "PASS"},
        {"test_id": "TEST-02", "result": "FAIL"},
        {"test_id": "TEST-03", "result": "VULNERABLE"},
    ]

    bfla_results = [
        {"test_id": "BFLA-01", "result": "PASS"},
        {"test_id": "BFLA-02", "result": "FAIL"},
        {"test_id": "BFLA-03", "result": "VULNERABLE"},
    ]

    with patch("scanner.main.__file__", str(tmp_path / "main.py")), \
         patch("scanner.main.load_config", return_value=config), \
         patch("scanner.main.check_api_connection", return_value=401), \
         patch("scanner.main.os.getenv", return_value="mock-token"), \
         patch("scanner.main.check_user_authentication",
               side_effect=[
                   (200, {"id": 1}),
                   (200, {"id": 2}),
               ]), \
         patch("scanner.main.check_order_access",
               side_effect=[
                   (200, {"user_id": 2}),
                   (403, {}),
               ]), \
         patch("scanner.main.run_bola_test",
               side_effect=bola_results) as bola_mock, \
         patch("scanner.main.run_bfla_test",
               side_effect=bfla_results) as bfla_mock:

        main()

    assert bola_mock.call_count == 3
    assert bfla_mock.call_count == 3

    bola_path = tmp_path / "reports" / "bola-results.json"
    bfla_path = tmp_path / "reports" / "bfla-results.json"

    assert bola_path.exists()
    assert bfla_path.exists()

    bola_report = json.loads(
        bola_path.read_text(encoding="utf-8")
    )

    bfla_report = json.loads(
        bfla_path.read_text(encoding="utf-8")
    )

    assert bola_report["target"] == config["base_url"]
    assert bola_report["total_tests"] == 3
    assert bola_report["summary"] == {
        "passed": 1,
        "failed": 1,
        "bola_findings": 1,
    }
    assert bola_report["test_results"] == bola_results

    assert bfla_report["target"] == bfla_config["base_url"]
    assert bfla_report["total_tests"] == 3
    assert bfla_report["summary"] == {
        "passed": 1,
        "failed": 1,
        "bfla_findings": 1,
    }
    assert bfla_report["test_results"] == bfla_results

    output = capsys.readouterr().out

    assert "API is reachable." in output
    assert "BOLA findings: 1" in output
    assert "BFLA findings: 1" in output