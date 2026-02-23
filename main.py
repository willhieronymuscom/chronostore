import time

from src.store import Store
from src.expiration.on_demand import OnDemandExpirationPolicy
from src.expiration.proactive import ProactiveExpirationPolicy


def demo_store(store: Store, label: str) -> None:
    """
    Simple demonstration that sets keys, waits,
    and prints store values before/after expiry.
    """
    print(f"\n--- Demo: {label} ---")
    store.set("foo", "bar", ttl_seconds=2)
    print("Set foo='bar' with TTL=2s")
    print("Immediate get:", store.get("foo"))

    print("Sleeping for 3 seconds…")
    time.sleep(3)

    val = store.get("foo")
    print("After sleep get:", val)


def main() -> None:
    print("ChronoStore TTL Key-Value Store Demo")

    # On-demand TTL policy
    on_demand = Store(expiration_policy=OnDemandExpirationPolicy())
    demo_store(on_demand, "On-Demand Expiration")

    # Proactive TTL policy
    proactive = Store(expiration_policy=ProactiveExpirationPolicy())
    demo_store(proactive, "Proactive Expiration")


if __name__ == "__main__":
    main()