# BOLA Test Cases

## Objective

Evaluate object-level authorization in REST API endpoints by sending requests with different authenticated user tokens.

## Test Environment

- Application: Laravel REST API
- Authentication: Laravel Sanctum (Bearer tokens)
- Database: PostgreSQL
- Test users: Alice (`user`), Bob (`user`), Admin (`admin`)
- Resource: Order
- Scope: Local Docker environment only

## Test Scenarios

| ID      | User            | Target Order  | Endpoint   | Expected Status |
|---------|-----------------|---------------|------------|-----------------|
| BOLA-01 | Alice           | Alice's order | Secure     | 200             |
| BOLA-02 | Alice           | Bob's order   | Secure     | 403             |
| BOLA-03 | Bob             | Alice's order | Secure     | 403             |
| BOLA-04 | Admin           | Bob's order   | Secure     | 200             |
| BOLA-05 | Alice           | Alice's order | Vulnerable | 200             |
| BOLA-06 | Alice           | Bob's order   | Vulnerable | 200             |
| BOLA-07 | Bob             | Alice's order | Vulnerable | 200             |
| BOLA-08 | Unauthenticated | Any order     | Vulnerable | 401             |

## Endpoint Definitions

Secure endpoint:

`GET /api/orders/{id}`

Vulnerable endpoint:

`GET /api/vulnerable/orders/{id}`

## Detection Logic

A potential BOLA vulnerability exists when:

1. The requester is authenticated.
2. The requested resource belongs to another user.
3. The access control policy does not permit the requester to view the resource.
4. The API returns the protected resource despite the missing permission.

For the controlled vulnerable endpoint, HTTP 200 with another user's order data indicates a successful unauthorized access attempt.

## Observed Results

The following scenarios were manually verified using Postman:

- Alice accessing Bob's order through the secure endpoint: HTTP 403.
- Alice accessing Bob's order through the vulnerable endpoint: HTTP 200.

Other scenarios remain available for additional testing.

## Automated BOLA Detection Results

The initial Python-based BOLA detection prototype was implemented and tested against the local Laravel REST API.

### Test Environment

- Scanner: Python 3
- API: Laravel with Sanctum authentication
- Database: PostgreSQL
- Test user: Alice (user ID 1)
- Target resource: Bob's order (order ID 3, user ID 2)
- Vulnerable endpoint: `GET /api/vulnerable-orders/{id}`
- Secure endpoint: `GET /api/orders/{id}`

### Automated Test Results

| Test ID | Endpoint | Actor | Resource Owner | Expected Status | Result |
|---|---|---|---|---|---|
| BOLA-06 | Vulnerable | Alice | Bob | 200 | BOLA detected |
| BOLA-02 | Secure | Alice | Bob | 403 | Access correctly denied |

### Detection Criteria

The scanner identifies a BOLA finding when:

1. The requester is authenticated.
2. The target resource belongs to another user.
3. The access-control policy prohibits access to that resource.
4. The API returns HTTP 200 and exposes the target resource.

### Conclusion

The prototype successfully detected the intentionally introduced BOLA vulnerability in the local testing environment.

The secure endpoint serves as a negative control for verifying correct authorization behavior.

The current implementation uses a predefined order ID. Future development will automate test-case execution and resource selection.

## Additional Test Results

| Test ID | Actual Status | Result                         |
|---------|---------------|--------------------------------|
| BOLA-03 | 403           | Access correctly denied        |
| BOLA-04 | 200           | Admin access correctly allowed |
| BOLA-07 | 200           | BOLA vulnerability reproduced  |

## Next Steps

- Test access using Bob's and Admin's tokens.
- Compare secure and vulnerable responses.
- Define structured test inputs for the Python scanner.
- Automate BOLA detection based on expected authorization rules.