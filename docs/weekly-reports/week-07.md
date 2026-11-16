# Week 7 — BFLA Implementation and Automated Security Testing

## 1. Objective

The objective of Week 7 was to investigate Broken Function Level Authorization (BFLA) vulnerabilities in REST APIs, implement controlled vulnerable and protected administrative functions, and extend the Python security scanner to detect BFLA automatically.

## 2. Implementation

Two Laravel controllers were implemented:

- `AdminOrderController` — provides access to the complete orders collection only to users with the `admin` role.
- `VulnerableAdminOrderController` — intentionally omits the administrator role check to demonstrate a BFLA vulnerability.

The following REST API endpoints were introduced:

| Endpoint | Description |
|---|---|
| `GET /api/admin/orders` | Protected administrative function |
| `GET /api/vulnerable-admin/orders` | Intentionally vulnerable administrative function |

Both endpoints use Laravel Sanctum authentication. The vulnerable endpoint is registered only in the local development environment.

## 3. Manual BFLA Testing

Manual security testing was performed using Postman with three user accounts: Alice, Bob, and Admin.

The protected administrative endpoint returned HTTP 403 for Alice and HTTP 200 for Admin.

The vulnerable administrative endpoint returned HTTP 200 for Alice, Bob, and Admin, demonstrating that regular users could execute an administrative function.

An unauthenticated request returned HTTP 401 when the `Accept: application/json` header was included.

## 4. Automated BFLA Test Cases

A configuration-driven BFLA testing framework was added to the existing Python scanner.

The following files were created or updated:

- `scanner/config/bfla-test-config.json` — configuration containing seven BFLA test cases.
- `scanner/main.py` — extended with `check_function_access()` and `run_bfla_test()` functions.

The scanner executes BFLA tests automatically, classifies results as `PASS`, `FAIL`, or `VULNERABLE`, and generates a structured JSON report.

### Automated Test Results

| Test ID | Actor | Endpoint | HTTP Status | Result |
|---|---|---|---|---|
| BFLA-01 | Alice | Protected | 403 | PASS |
| BFLA-02 | Bob | Protected | 403 | PASS |
| BFLA-03 | Admin | Protected | 200 | PASS |
| BFLA-04 | Alice | Vulnerable | 200 | VULNERABLE |
| BFLA-05 | Bob | Vulnerable | 200 | VULNERABLE |
| BFLA-06 | Admin | Vulnerable | 200 | PASS |
| BFLA-07 | Unauthenticated | Vulnerable | 401 | PASS |

### Summary

- Total test cases: **7**
- Passed: **5**
- Failed: **0**
- BFLA findings: **2**

The two findings represent separate unauthorized access scenarios involving one intentionally vulnerable administrative function.

## 5. JSON Reporting

The scanner generates a separate BFLA report:

`scanner/reports/bfla-results.json`

The report contains the target API, total number of tests, summary statistics, and individual test results.

The existing BOLA testing functionality and its JSON reporting remain part of the scanner.

## 6. Key Findings

The experiments demonstrated that authentication alone does not guarantee function-level authorization.

Although Laravel Sanctum successfully rejected unauthenticated requests, regular authenticated users could execute the intentionally vulnerable administrative function because the role-based authorization check was missing.

The protected administrative endpoint correctly enforced the required access restrictions.

## 7. Conclusion

Week 7 successfully implemented and tested a controlled BFLA vulnerability and extended the Python security scanner with automated BFLA detection.

The project now supports automated security testing for two OWASP API authorization vulnerability categories:

- Broken Object Level Authorization (BOLA)
- Broken Function Level Authorization (BFLA)

## 8. Next Steps

Week 8 will focus on expanding authentication and authorization test contexts, improving detection accuracy, and strengthening the integration of BOLA and BFLA testing within the scanner.