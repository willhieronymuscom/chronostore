# Exercise: In-Memory Key-Value Store with TTL

## Problem Statement

Implement a simple **in-memory key-value store** with **TTL (time-to-live)** functionality.

---

## Requirements

- Support `set(key, value, ttl_seconds)` to store a value with a TTL.
- Support `get(key)` to retrieve the value; return `None` (or equivalent) if expired or missing.
- TTL should be based on the current timestamp (seconds or milliseconds).
- Store everything in memory (no external databases).

---

## Project Notes

ChronoStore is implemented in Python 3.12+ and uses uv for package and dependency management
via pyproject.toml.

## Tooling & Environment

- Language: Python (>= 3.12)
- Package management: uv
- Testing: pytest
- Coverage: pytest-cov
- Runtime dependencies: none

## Common Commands

Testing:

- make test
- make coverage
- make coverage-report [html report]

Demo:

- make demo
