from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.store import Store


class ExpirationPolicy(ABC):
    """
    Base class for expiration policies with TTL logic factored in.
    """

    def compute_expires_at(self, now: int, ttl_seconds: int) -> int:
        """
        Default TTL computation: absolute expiry at `now + ttl_seconds`.
        """
        return now + ttl_seconds

    def is_expired(self, now: int, expires_at: int) -> bool:
        """
        Default expiration test: expired if now >= expires_at.
        """
        return now >= expires_at

    @abstractmethod
    def on_set(self, store: "Store", key: str, expires_at: int) -> None:
        """
        Optional per-policy state updates after set.
        """
        ...

    @abstractmethod
    def cleanup(
        self,
        store: "Store",
        now: int,
        *,
        key: str | None = None
    ) -> None:
        """
        Perform cleanup based on this policy.
        """
        ...