# API Authentication Architecture

## Overview

The test REST API is implemented using Laravel and PostgreSQL. Laravel Sanctum provides token-based authentication.

The application currently supports three test users with two roles: `user` and `admin`.

## Test Users

| User  | Email              | Role  |
|-------|--------------------|-------|
| Alice | alice@example.test | user  |
| Bob   | bob@example.test   | user  |
| Admin | admin@example.test | admin |

These accounts are used exclusively in the local testing environment.

## Authentication Flow

1. The client sends an HTTP POST request to `/api/login` with an email and password.
2. Laravel validates the submitted credentials.
3. If authentication succeeds, Sanctum generates an API token.
4. The client includes the token in later requests using the `Authorization: Bearer <token>` header.
5. The `auth:sanctum` middleware authenticates the request.
6. The protected endpoint returns the authenticated user's information.

## API Endpoints

### POST /api/login

Authenticates a user and returns an API token.

**Successful response:** `200 OK`

**Invalid credentials:** `401 Unauthorized`

### GET /api/user

Returns information about the authenticated user.

**Valid token:** `200 OK`

**Missing or invalid token:** `401 Unauthorized`

## User Roles

The `users` table contains a `role` column.

Supported roles:

- `user` — standard application user.
- `admin` — administrator.

The default role is `user`.

The `role` attribute is intentionally excluded from the model's mass-assignable fields to reduce the risk of unintended privilege assignment.

Role-based authorization checks have not yet been implemented.

## Database Changes

The following database changes were introduced during Week 3:

- Added the `role` column to the `users` table.
- Created the `personal_access_tokens` table through Laravel Sanctum.
- Seeded three test users: Alice, Bob, and Admin.

## Security Considerations

- Passwords are stored as hashes.
- Passwords and remember tokens are excluded from serialized user data.
- Protected endpoints require authentication.
- Invalid login credentials do not produce API tokens.
- Login requests are rate-limited.
- API tokens must not be committed to GitHub or included in public documentation.

## Current Limitations

The application currently implements authentication but does not yet enforce object-level or function-level authorization.

Order resources and vulnerability test scenarios will be introduced in later development stages.
