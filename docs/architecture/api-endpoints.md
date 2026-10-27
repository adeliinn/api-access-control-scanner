# REST API Endpoints

## Authentication

The API uses Laravel Sanctum with Bearer tokens.

### POST /api/login

Authenticates a user and returns an API token.

### GET /api/user

Returns information about the authenticated user.

## Orders API

All order endpoints require authentication via `auth:sanctum`.

| Method | Endpoint         | Description            |
|--------|------------------|------------------------|
| GET    | /api/orders      | List accessible orders |
| GET    | /api/orders/{id} | View a specific order  |
| POST   | /api/orders      | Create an order        |
| PUT    | /api/orders/{id} | Update an order        |
| DELETE | /api/orders/{id} | Delete an order        |

## Authorization Rules

### Regular User

- Can view only their own orders.
- Can create orders assigned to their own account.
- Can update only their own orders.
- Can delete only their own orders.
- Cannot access another user's orders.

### Administrator

- Can view all orders.
- Can create orders.
- Can update any order.
- Can delete any order.

## HTTP Status Codes

| Status | Meaning                 |
|--------|-------------------------|
| 200    | Successful request      |
| 201    | Resource created        |
| 204    | Resource deleted        |
| 401    | Authentication required |
| 403    | Access denied           |
| 404    | Resource not found      |
| 422    | Validation failed       |

## Security Mechanisms

- Laravel Sanctum authenticates API requests.
- OrderPolicy checks object-level authorization.
- The server assigns order ownership.
- Client-provided `user_id` is ignored during order creation.
- Update operations accept only validated fields.
- Unauthorized update and delete operations are rejected.

## BOLA Testing Scenarios

1. Alice requests Bob's order.
   Expected: 403 Forbidden.

2. Bob attempts to update Alice's order.
   Expected: 403 Forbidden.

3. Bob attempts to delete Alice's order.
   Expected: 403 Forbidden.

4. Alice submits a new order with Bob's user_id.
   Expected: the order belongs to Alice.

These scenarios will be used as a baseline for automated
access-control testing.