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
