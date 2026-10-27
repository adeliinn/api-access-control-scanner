# Week 4 — Order Management and Access Control

## Current Progress

- Created the `Order` model and database migration
- Added the `orders` table with `user_id`, `description`, `amount`, and `status` fields
- Established relationships between users and orders using Eloquent ORM
- Created test orders for Alice and Bob using `OrderSeeder`
- Defined role-based and object-level access control rules for `user` and `admin`
- Implemented the `OrderPolicy` with `viewAny`, `view`, `create`, `update`, and `delete` permissions
- Developed REST API endpoints for listing, viewing, creating, updating, and deleting orders
- Protected all order endpoints using Laravel Sanctum authentication
- Verified that regular users can access only their own orders
- Verified that administrators can access orders belonging to different users
- Tested unauthorized access to other users' orders (`403 Forbidden`)
- Verified that users cannot assign orders to another account by modifying `user_id`
- Tested order creation (`201 Created`), updating (`200 OK`), and deletion (`204 No Content`)
- Documented the access control model and REST API endpoints

## Next Steps

- Expand test scenarios for object-level authorization
- Prepare a separate, intentionally vulnerable API endpoint for controlled BOLA/IDOR testing
- Compare secure and vulnerable API behavior using different user tokens
- Introduce function-level authorization scenarios for BFLA testing
- Document expected and actual HTTP responses for security tests
- Prepare the foundation for automated access control testing with Python