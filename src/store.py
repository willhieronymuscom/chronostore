import time
from typing import Any

from src.expiration.base import ExpirationPolicy


class Store:
    def __init__(
        self,
        expiration_policy: ExpirationPolicy,
        clock: callable = None,
    ) -> None:
        self._values: dict[str, Any] = {}
        self._expires: dict[str, float] = {}
        self._policy = expiration_policy
        self._clock = clock if clock is not None else time.time

    def set(self, key: str, value: Any, ttl_seconds: float) -> None:
        """
        Store a value with TTL. If ttl_seconds <= 0 or
        computed expiry is already in the past, the key
        is treated as expired (no-op or deletion).
        """
        now = self._clock()
        expires_at = self._policy.compute_expires_at(now, ttl_seconds)

        # If expired immediately, delete and return
        if expires_at <= now:
            self._delete_key(key)
            return

        # Write the value and expiry
        self._values[key] = value
        self._expires[key] = expires_at

        # Let the policy track the set
        self._policy.on_set(self, key, expires_at)

    def get(self, key: str) -> Any | None:
        """
        Retrieve value or None if missing/expired.
        Always runs policy cleanup before checking.
        """
        now = self._clock()

        # Perform cleanup via policy
        self._policy.cleanup(self, now, key=key)

        # After cleanup, check existence
        if key not in self._values:
            return None

        return self._values[key]

    def _delete_key(self, key: str) -> None:
        """
        Internal helper to remove a key from the store.
        """
        self._values.pop(key, None)
        self._expires.pop(key, None)