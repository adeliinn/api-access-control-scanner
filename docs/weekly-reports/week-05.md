# Week 5 Report — BOLA Vulnerability Simulation and Initial Automated Detection

## 1. Objective

The objective of Week 5 was to create a controlled Broken Object Level Authorization (BOLA) vulnerability in the REST API and implement an initial Python-based scanner capable of detecting unauthorized access to API resources.

## 2. Tasks Completed

- Implemented an intentionally vulnerable API endpoint for retrieving orders.
- Restricted the vulnerable endpoint to the local development environment.
- Tested authorized and unauthorized access using Postman.
- Defined BOLA test scenarios and expected HTTP responses.
- Created a JSON configuration file for the scanner.
- Configured Python virtual environment and authentication tokens.
- Implemented API connectivity and authentication checks.
- Developed an initial automated BOLA detection test.
- Added a verification test for the protected API endpoint.

## 3. Implementation Details

The Laravel application exposes two endpoints:

- Secure: `GET /api/orders/{id}`
- Vulnerable: `GET /api/vulnerable-orders/{id}`

The secure endpoint enforces resource-level authorization through `OrderPolicy`.

The intentionally vulnerable endpoint retrieves an order without checking whether the authenticated user is authorized to access it.

The Python scanner uses HTTP requests with Sanctum bearer tokens to compare access behavior between the two endpoints.

## 4. Testing Methodology

Testing was performed using Alice, Bob, and Admin accounts.

The main automated scenario involved Alice attempting to access Bob's order with ID 3.

The scanner checks the HTTP response status and confirms the resource owner's `user_id` before reporting a BOLA finding.

## 5. Results

| Test | Expected | Observed |
|---|---|---|
| API connectivity without authentication | HTTP 401 | HTTP 401 |
| Alice, Bob, and Admin authentication | Successful | Successful |
| Alice accesses Bob's order through vulnerable endpoint | HTTP 200 | HTTP 200; BOLA detected |
| Alice accesses Bob's order through secure endpoint | HTTP 403 | HTTP 403; access denied |

The initial prototype successfully identified the deliberately introduced vulnerability while recognizing the correct denial of unauthorized access by the protected endpoint.

## 6. Challenges and Solutions

**Incorrect endpoint URL:** The scanner initially received HTTP 404 because its configured vulnerable endpoint differed from the Laravel route. The JSON configuration was corrected.

**Python indentation error:** An indentation issue occurred while adding secure API verification. The code structure was corrected.

**Token security:** Authentication tokens were stored in a local `.env` file excluded from Git tracking. Previously exposed test tokens were revoked and replaced.

## 7. Deliverables

- `api/app/Http/Controllers/Api/VulnerableOrderController.php`
- Updated `api/routes/api.php`
- `docs/research/bola-test-cases.md`
- `scanner/config/bola-test-config.json`
- `scanner/main.py`
- Screenshot of automated BOLA detection results
- Week 5 report

## 8. Conclusion and Next Steps

Week 5 established a controlled testing environment for BOLA vulnerabilities and demonstrated the feasibility of automated detection using Python.

The scanner currently verifies a predefined cross-user access scenario. The next development stage will focus on executing multiple test cases automatically, reducing hardcoded values, and generating structured vulnerability findings.