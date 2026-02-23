from typing import TYPE_CHECKING

from src.expiration.base import ExpirationPolicy

if TYPE_CHECKING:
    from src.store import Store


class OnDemandExpirationPolicy(ExpirationPolicy):
    """
    Expire only on access for the given key.
    """

    def on_set(self, store: "Store", key: str, expires_at: int) -> None:
        # Nothing extra to track on set
        pass

    def cleanup(
        self,
        store: "Store",
        now: int,
        *,
        key: str | None = None
    ) -> None:
        # OnDemand cleanup keeps access at O(1)
        if key is None:
            return

        expires_at = store._expires.get(key)
        if expires_at is None:
            return

        if self.is_expired(now, expires_at):
            store._delete_key(key)