import json
import os
from dotenv import load_dotenv
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


CONFIG_PATH = (
    Path(__file__).resolve().parent
    / "config"
    / "bola-test-config.json"
)

load_dotenv(Path(__file__).resolve().parent / ".env")

def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def check_api_connection(base_url):
    url = base_url.rstrip("/") + "/api/user"

    request = Request(
        url,
        headers={"Accept": "application/json"},
        method="GET",
    )

    try:
        with urlopen(request, timeout=5) as response:
            return response.status

    except HTTPError as error:
        return error.code

    except URLError as error:
        print(f"Connection error: {error.reason}")
        return None


def check_user_authentication(base_url, token):
    url = base_url.rstrip("/") + "/api/user"

    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.load(response)

    except HTTPError as error:
        return error.code, {}

    except URLError as error:
        print(f"Connection error: {error.reason}")
        return None, {}




def check_order_access(base_url, endpoint, order_id, token):
    url = (
        base_url.rstrip("/")
        + endpoint.replace("{id}", str(order_id))
    )

    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.load(response)

    except HTTPError as error:
        return error.code, {}

    except URLError as error:
        print(f"Connection error: {error.reason}")
        return None, {}




def run_bola_test(base_url, config, test_case):
    test_id = test_case["id"]
    actor = test_case["actor"]
    resource_owner = test_case["resource_owner"]
    endpoint_name = test_case["endpoint"]

    actor_config = config["users"][actor]
    token = os.getenv(actor_config["token_env"])

    if not token:
            print(f"[FAIL] {test_id}: Token for {actor} is missing.")

            return {
                "test_id": test_id,
                "actor": actor,
                "resource_owner": resource_owner,
                "order_id": None,
                "endpoint": endpoint_name,
                "expected_status": test_case["expected_status"],
                "actual_status": None,
                "result": "FAIL",
                "error": "Authentication token is missing",
            }

    order_id = config["resources"][f"{resource_owner}_order_id"]
    endpoint = config["endpoints"][endpoint_name]

    status, data = check_order_access(
        base_url,
        endpoint,
        order_id,
        token,
    )


    expected_status = test_case["expected_status"]
    expected_owner_id = config["users"][resource_owner]["user_id"]

    if status is None:
        result = "FAIL"

    elif status != expected_status:
        result = "FAIL"

    elif status == 200 and data.get("user_id") != expected_owner_id:
        result = "FAIL"

    elif (
        test_case.get("expected_finding") == "BOLA"
        and actor != resource_owner
        and actor_config["role"] != "admin"
        and status == 200
        and data.get("user_id") == expected_owner_id
    ):
        result = "VULNERABLE"

    else:
        result = "PASS"

    print(
        f"[{result}] {test_id}: "
        f"{actor} -> {resource_owner}'s order "
        f"(ID {order_id}), endpoint={endpoint_name}, "
        f"HTTP {status}, expected {expected_status}"
    )

    return {
        "test_id": test_id,
        "actor": actor,
        "resource_owner": resource_owner,
        "order_id": order_id,
        "endpoint": endpoint_name,
        "expected_status": expected_status,
        "actual_status": status,
        "result": result,
    }




def main():
    print("=== BOLA Scanner ===")

    config = load_config()
    base_url = config["base_url"]

    print(f"Target API: {base_url}")
    print(f"Loaded test cases: {len(config['test_cases'])}")

    status = check_api_connection(base_url)

    if status == 401:
        print("API is reachable.")
        print("Authentication is required (HTTP 401).")

    elif status is None:
        print("Could not connect to the API.")
        return

    else:
        print(f"API returned HTTP {status}.")
        return

    # Authentication tests
    print("\n=== Authentication Tests ===")

    for username, user_config in config["users"].items():
        token = os.getenv(user_config["token_env"])

        if not token:
            print(f"{username}: token is missing")
            continue

        status, data = check_user_authentication(base_url, token)

        if status == 200:
            expected_id = user_config["user_id"]
            actual_id = data.get("id")

            if actual_id == expected_id:
                print(f"{username}: authenticated successfully")
            else:
                print(
                    f"{username}: user ID mismatch "
                    f"(expected {expected_id}, got {actual_id})"
                )
        else:
            print(f"{username}: HTTP {status}")


    print("\n=== BOLA Detection Test ===")

    alice_token = os.getenv("ALICE_TOKEN")

    alice_order_id = config["resources"]["alice_order_id"]
    bob_order_id = config["resources"]["bob_order_id"]

    if alice_token:
        status, data = check_order_access(
            base_url,
            config["endpoints"]["vulnerable"],
            bob_order_id,
            alice_token,
        )

        if status == 200 and data.get("user_id") == config["users"]["bob"]["user_id"]:
            print("[VULNERABLE] BOLA detected!")
            print("Alice accessed Bob's order.")
            print(f"Order ID: {bob_order_id}")

        elif status == 200:
            print("[INFO] HTTP 200, but Bob's ownership was not confirmed.")

        else:
            print(f"[INFO] HTTP {status}. BOLA not confirmed.")
    else:
        print("[ERROR] Alice token is missing.")



    print("\n=== Secure API Verification ===")

    if alice_token:
        secure_status, secure_data = check_order_access(
            base_url,
            config["endpoints"]["secure"],
            bob_order_id,
            alice_token,
        )

        if secure_status == 403:
            print("[PROTECTED] Access correctly denied.")
            print("Alice cannot access Bob's order.")

        elif secure_status == 200:
            if secure_data.get("user_id") == config["users"]["bob"]["user_id"]:
                print("[WARNING] Possible BOLA in secure endpoint!")
            else:
                print("[INFO] HTTP 200, but Bob's ownership was not confirmed.")

        else:
            print(f"[INFO] Unexpected HTTP status: {secure_status}")
    else:
        print("[ERROR] Alice token is missing.")




    print("\n=== Automated BOLA Test Cases ===")

    results = {
        "PASS": 0,
        "FAIL": 0,
        "VULNERABLE": 0,
    }


    test_results = []

    for test_case in config["test_cases"]:
        test_result = run_bola_test(base_url, config, test_case)

        if test_result is None:
            results["FAIL"] += 1
            continue

        test_results.append(test_result)

        result = test_result["result"]

        if result in results:
            results[result] += 1
        else:
            results["FAIL"] += 1


    print("\n=== Test Summary ===")
    print(f"Total tests: {len(config['test_cases'])}")
    print(f"Passed: {results['PASS']}")
    print(f"Failed: {results['FAIL']}")
    print(f"BOLA findings: {results['VULNERABLE']}")




    # Save scan results to JSON
    report_dir = Path(__file__).resolve().parent / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / "bola-results.json"

    report = {
        "target": base_url,
        "total_tests": len(config["test_cases"]),
        "summary": {
            "passed": results["PASS"],
            "failed": results["FAIL"],
            "bola_findings": results["VULNERABLE"],
        },
        "test_results": test_results,
    }

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print(f"\nReport saved to: {report_path}")




if __name__ == "__main__":
    main()
