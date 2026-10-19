# Authentication vs. Authorization in REST APIs

## Purpose

This document explains the distinction between authentication and authorization and its relevance to automated access control vulnerability detection.

## Authentication

Authentication determines the identity of the client making an API request.

In the current test application, Laravel Sanctum provides token-based authentication.

A user submits valid credentials to `/api/login`, receives a token, and uses that token to access protected endpoints.

A request without valid authentication credentials is rejected with HTTP `401 Unauthorized`.

## Authorization

Authorization determines whether an authenticated user has permission to perform a particular action or access a particular resource.

Successful authentication does not automatically imply permission to access all API resources.

For example, Alice and Bob may both have valid API tokens, but Bob should not automatically be allowed to access an order belonging to Alice.

## Broken Object Level Authorization (BOLA)

BOLA occurs when an API fails to enforce authorization for a specific object.

Example scenario:

- Alice owns Order 1.
- Bob authenticates using his own valid token.
- Bob requests `GET /api/orders/1`.
- The API must verify whether Bob is authorized to access that order.

If the API exposes Alice's order to Bob without permission, this represents a potential BOLA vulnerability.

## Broken Function Level Authorization (BFLA)

BFLA occurs when an API fails to enforce appropriate permissions for an operation.

Example scenario:

- An administrative endpoint is intended for users with the `admin` role.
- Bob authenticates as a regular user.
- Bob attempts to access the administrative endpoint.
- The API must reject the request if Bob lacks the required permissions.

## Relevance to the Scanner

The future Python scanner will test authorization by sending requests in different authenticated contexts.

The planned approach includes:

1. Authenticating as different test users.
2. Identifying resources and operations associated with specific users or roles.
3. Sending requests with different API tokens.
4. Comparing observed HTTP responses with expected access control rules.
5. Reporting potential authorization violations.

## Week 3 Outcome

During Week 3, the authentication infrastructure was implemented and tested.

The application now supports multiple authenticated identities, providing the foundation for automated authorization testing.

Actual BOLA and BFLA test scenarios will be implemented in later weeks.
