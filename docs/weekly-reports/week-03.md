# Week 3 — User Roles and API Authentication

## Current Progress

- Added the `role` column to the `users` table using a Laravel migration
- Defined two user roles: `user` and `admin`
- Installed and configured Laravel Sanctum for token-based API authentication
- Updated the User model to support API tokens using the `HasApiTokens` trait
- Created three test users: Alice, Bob, and Admin
- Implemented the `POST /api/login` endpoint for user authentication
- Added rate limiting to the login endpoint
- Configured the protected `GET /api/user` endpoint
- Verified successful authentication with valid credentials (`200 OK`)
- Verified rejection of invalid credentials (`401 Unauthorized`)
- Tested access to protected endpoints with and without a valid Bearer token
- Documented the authentication architecture and the differences between authentication and authorization

## Next Steps

- Create the Order model and database migration
- Establish relationships between users and orders
- Implement REST API endpoints for order management
- Define object-level and function-level access control rules
- Introduce the first controlled BOLA/IDOR vulnerability scenario
- Prepare test requests for comparing access between Alice and Bob