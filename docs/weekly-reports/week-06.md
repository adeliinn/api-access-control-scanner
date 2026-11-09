# Week 6 Report — Automated BOLA Testing and Structured JSON Reporting

## 1. Objective

The objective of Week 6 was to extend the initial Python-based BOLA scanner by automating the execution of multiple access control test cases, reducing hardcoded resource identifiers, classifying test outcomes, and generating structured JSON reports.

## 2. Tasks Completed

- Extended the scanner configuration with resource identifiers for Alice and Bob.
- Implemented automated execution of BOLA test cases defined in JSON.
- Added support for different actors, resource owners, and API endpoints.
- Implemented classification of test results as `PASS`, `FAIL`, or `VULNERABLE`.
- Added automatic calculation of test statistics.
- Modified the scanner to return structured results for individual test cases.
- Implemented automatic generation of a JSON scan report.
- Added error handling for missing authentication tokens.
- Updated `.gitignore` to exclude generated JSON reports from Git tracking.

## 3. Implementation Details

The scanner uses the configuration file:

`scanner/config/bola-test-config.json`

The configuration defines users, authentication token environment variables, resource identifiers, API endpoints, and test cases.

The `run_bola_test()` function automatically retrieves the required parameters, sends an authenticated HTTP request, evaluates the response status and resource ownership, and classifies the result.

Three result categories are supported:

- `PASS`: The test produced the expected authorization behavior.
- `FAIL`: The test failed because of an unexpected response or an execution error.
- `VULNERABLE`: Unauthorized access to another user's resource was confirmed.

The scanner saves structured results to:

`scanner/reports/bola-results.json`

The report contains the target API address, total number of tests, summary statistics, and individual test results.

## 4. Testing Methodology

Testing was performed against the Laravel REST API using three accounts: Alice, Bob, and Admin.

The following endpoints were tested:

- Secure: `GET /api/orders/{id}`
- Vulnerable: `GET /api/vulnerable-orders/{id}`

Five automated test cases were executed to evaluate access control behavior across different users and endpoints.

The scanner compared actual HTTP responses with expected results and verified resource ownership where applicable.

An additional negative test was performed to evaluate the handling of a missing authentication token.

## 5. Results

| Test | Expected | Observed |
|---|---|---|
| BOLA-02: Alice accesses Bob's order through secure endpoint | HTTP 403 | HTTP 403; PASS |
| BOLA-03: Bob accesses Alice's order through secure endpoint | HTTP 403 | HTTP 403; PASS |
| BOLA-04: Admin accesses Bob's order through secure endpoint | HTTP 200 | HTTP 200; PASS |
| BOLA-06: Alice accesses Bob's order through vulnerable endpoint | HTTP 200; BOLA | HTTP 200; VULNERABLE |
| BOLA-07: Bob accesses Alice's order through vulnerable endpoint | HTTP 200; BOLA | HTTP 200; VULNERABLE |

**Test summary:**

- Total tests: 5
- Passed: 3
- Failed: 0
- BOLA findings: 2

The two BOLA findings represent two test scenarios involving the same intentionally vulnerable endpoint.

The scanner successfully generated a JSON report containing the results of all five automated tests.

## 6. Challenges and Solutions

**Hardcoded resource identifiers:** The initial scanner relied on predefined order IDs. Resource identifiers were moved to the JSON configuration file.

**Manual test execution:** The initial prototype executed a limited predefined scenario. A configuration-driven test execution function was implemented to support multiple scenarios.

**Result classification:** HTTP status codes alone were insufficient to describe test outcomes. The scanner was extended to classify results using expected responses and resource ownership information.

**Missing authentication tokens:** Tests with unavailable tokens initially did not produce detailed result records. Error handling was improved to record these cases as `FAIL`.

**Generated report management:** Automatically generated JSON reports were excluded from Git tracking using `.gitignore`.

## 7. Deliverables

- Updated `scanner/config/bola-test-config.json`
- Updated `scanner/main.py`
- Updated `.gitignore`
- Automated execution of five BOLA test cases
- Structured JSON scan report: `scanner/reports/bola-results.json`
- Week 6 report

## 8. Conclusion and Next Steps

Week 6 successfully extended the initial BOLA scanner into a configuration-driven automated testing tool.

The scanner now executes multiple access control scenarios, classifies results, calculates summary statistics, handles missing authentication tokens, and generates structured JSON reports.

The next development stage will focus on expanding test coverage, improving vulnerability detection logic, and preparing the scanner for systematic evaluation.