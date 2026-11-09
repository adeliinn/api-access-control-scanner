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

    bob_order_id = 3

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




if __name__ == "__main__":
    main()
