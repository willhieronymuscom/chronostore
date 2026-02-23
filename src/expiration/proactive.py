import heapq
from typing import TYPE_CHECKING

from src.expiration.base import ExpirationPolicy

if TYPE_CHECKING:
    from src.store import Store


class ProactiveExpirationPolicy(ExpirationPolicy):
    """
    Proactively expire keys ordered by expiry time using a min-heap.
    """

    def __init__(self) -> None:
        self._heap: list[tuple[int, str]] = []

    def on_set(
        self,
        store: "Store",
        key: str,
        expires_at: int
    ) -> None:
        """
        Proactive on set costs OLog n) to update
        the binary tree
        """
        # Proactive on set
        # push expired/key to heap
        heapq.heappush(self._heap, (expires_at, key))

    def cleanup(
        self,
        store: "Store",
        now: int,
        *,
        key: str | None = None
    ) -> None:
        """
        Remove all expired keys at the top of the heap.
        Only delete if the heap entry matches the store’s current expiry.

        Proactive cleanup costs "get" O(log n)
        """
        while self._heap:
            # peak at current top
            expires_at_top, key_top = self._heap[0]

            # Stop when we hit an unexpired item
            if not self.is_expired(now, expires_at_top):
                break

            heapq.heappop(self._heap)

            current_expires_at = store._expires.get(key_top)

            # Skip if key has been deleted or expiry doesn't match
            if current_expires_at is None or current_expires_at != expires_at_top:
                continue

            store._delete_key(key_top)