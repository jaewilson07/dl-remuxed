---
applyTo: '**/*'
name: error_design_instructions
description: Global error hierarchy and usage patterns for domolibrary2.
---

> Last updated: 2025-11-17

# Domo Library Error Design Strategy

## Overview

This document defines stable, high-level guidelines for error naming and usage
in domolibrary2. The goal is to avoid drift and keep the rules simple enough
that they rarely need to change.

## Core Error Hierarchy

All library-specific exceptions must inherit (directly or indirectly) from
`DomoError` defined in `src/domolibrary2/base/exceptions.py`.

High‑level hierarchy:

- `DomoError`: base for all Domo-related errors
  - `RouteError`: API route/endpoint errors
  - `ClassError`: class instance errors (entity/manager classes)
  - `AuthError`: authentication-specific errors

When adding new errors, prefer extending one of these three specializations
instead of inheriting from `DomoError` directly.

## Naming Conventions

- **Style**: Use CamelCase for all error class names.
- **Suffix**: All error class names **must end with `Error`**.
- **Scope**: Names should describe the failure domain and/or action
  (for example `DatasetGetError`, `UserCrudError`, `SearchUserNotFoundError`).
- **Uniqueness**: Do not create multiple error types for the same logical
  failure mode—prefer a single reusable error type.

We do not require a rigid per-module taxonomy here; follow these conventions
and keep names descriptive and consistent with nearby code.

## Catching and Raising Errors

- **Never** catch bare `Exception` inside library code.
- Prefer catching `DomoError` or one of its subclasses. This ensures we do
  not accidentally swallow unexpected runtime errors (e.g. `TypeError`,
  `ValueError`, `KeyError`).
- When you need a broad catch for library errors, use:

  ```python
  try:
      ...
  except DomoError as exc:
      ...  # log, translate, or re-raise
  ```

- Only catch more specific subclasses when you genuinely need to handle
  that failure mode differently.

When raising errors:

- Always raise a `DomoError` subclass, never a bare `Exception`.
- Include relevant context such as entity IDs, operation names, and the
  underlying API response (when available) via the standard constructor
  parameters defined on `DomoError` / `RouteError`.

## Route and Class Errors

Route modules and entity/manager classes should follow these guidelines:

- Route functions should raise `RouteError` subclasses when HTTP calls fail
  or responses are invalid.
- Entity and manager methods should raise `ClassError` subclasses for
  domain-level problems that are not strictly HTTP failures.
- Authentication flows should raise `AuthError` subclasses.

Prefer reusing existing error types in the relevant module. Only introduce a
new error subclass when you need a distinct failure mode that callers can
reasonably be expected to handle separately.

## Error Message Guidelines

Error messages should be:

- **Specific**: include IDs, operation names, and key input parameters.
- **Actionable**: when possible, hint at what the caller or user can do
  (for example "verify dataset exists and you have read permission").
- **Contextual**: when wrapping an HTTP response, preserve useful pieces of
  the original API message for debugging.

Avoid leaking secrets or sensitive credentials in error messages or logs.

## Documentation and Maintenance

- This document intentionally avoids enumerating every concrete error class
  to reduce the risk of drift as the code evolves.
- For examples of concrete error implementations, refer to existing
  route and class modules under `src/domolibrary2/routes/` and
  `src/domolibrary2/classes/`.
- When adding new error types, ensure they follow the hierarchy and naming
  rules above; detailed examples belong in code, not in this document.

These guidelines are intended to stay stable over time so that error handling
remains consistent, debuggable, and maintainable across the entire library.
