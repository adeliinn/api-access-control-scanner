# Week 5 — BOLA Vulnerability Simulation and Initial Automated Detection

## Current Progress

- Implemented the `VulnerableOrderController` to simulate a controlled BOLA vulnerability
- Created the intentionally vulnerable `GET /api/vulnerable-orders/{id}` endpoint
- Restricted the vulnerable endpoint to the local development environment
- Compared protected and vulnerable API behavior using Postman
- Verified unauthorized cross-user resource access through the vulnerable endpoint (`200 OK`)
- Verified correct access denial through the protected endpoint (`403 Forbidden`)
- Documented BOLA test scenarios and expected HTTP responses
- Configured the Python virtual environment for the security scanner
- Created the `bola-test-config.json` configuration file
- Configured secure storage of authentication tokens using a local `.env` file
- Implemented API connectivity and authentication checks for Alice, Bob, and Admin
- Developed the initial Python-based automated BOLA detection algorithm
- Implemented resource ownership verification using the returned `user_id`
- Successfully detected the intentionally introduced BOLA vulnerability
- Verified correct authorization behavior of the protected endpoint

## Next Steps

- Automate the execution of multiple BOLA test cases
- Move hardcoded resource identifiers to the JSON configuration
- Support different actors, resource owners, and API endpoints
- Implement automated classification of test results
- Add automatic calculation of test statistics
- Implement structured JSON vulnerability reporting
- Improve authentication token error handling