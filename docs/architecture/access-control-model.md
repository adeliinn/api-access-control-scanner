# Access Control Model

## Overview

The test REST API uses role-based and ownership-based access control.

Two roles are defined:

- `user` — a regular authenticated user.
- `admin` — an administrator with access to all test orders.

Each order belongs to one user through the `user_id` foreign key.

## Authorization Rules

| Operation | Regular User | Administrator |
|---|---|---|
| View own orders | Allow | Allow |
| View another user's orders | Deny | Allow |
| Create an order | Allow | Allow |
| Update own orders | Allow | Allow |
| Update another user's orders | Deny | Allow |
| Delete own orders | Allow | Allow |
| Delete another user's orders | Deny | Allow |
| List orders | Own orders only | All orders |
| Access administrative functions | Deny | Allow |

## BOLA Test Scenario

A regular user attempts to access an order belonging to another user by changing the order identifier in an API request.

Expected behavior: access is denied.

## BFLA Test Scenario

A regular user attempts to access an administrator-only API endpoint.

Expected behavior: access is denied.

## Current Implementation Status

User roles, API authentication, the Order model, database relationships, and test orders have been created.

The authorization rules described above are design requirements and have not yet been implemented in API controllers or policies.