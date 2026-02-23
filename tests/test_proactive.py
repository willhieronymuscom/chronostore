import pytest

from src.expiration.proactive import ProactiveExpirationPolicy
from src.store import Store


def test_set_and_get_not_expired(fake_clock):
    policy = ProactiveExpirationPolicy()
    store = Store(expiration_policy=policy, clock=fake_clock)

    store.set("k1", "v1", ttl_seconds=5)
    assert store.get("k1") == "v1"


def test_proactive_cleans_expired_without_get_on_same_key(fake_clock):
    policy = ProactiveExpirationPolicy()
    store = Store(expiration_policy=policy, clock=fake_clock)

    store.set("a", "A", ttl_seconds=5)
    store.set("b", "B", ttl_seconds=10)

    # Advance past "a", but not "b"
    fake_clock.advance(6)

    # Trigger proactive cleanup (invoked inside get; can be any key)
    result = store.get("b")

    # "a" should be gone, "b" should still be present
    assert store.get("a") is None
    assert result == "B"


def test_repeated_set_updates_heap_correctly(fake_clock):
    policy = ProactiveExpirationPolicy()
    store = Store(expiration_policy=policy, clock=fake_clock)

    # Set key with short TTL
    store.set("x", "v1", ttl_seconds=2)

    # Before expiration, reset with longer TTL
    fake_clock.advance(1)
    store.set("x", "v2", ttl_seconds=10)

    # Advance beyond the first expiry
    fake_clock.advance(2)

    # Calling get should NOT delete key "x"
    assert store.get("x") == "v2"


def test_multiple_expirations(fake_clock):
    policy = ProactiveExpirationPolicy()
    store = Store(expiration_policy=policy, clock=fake_clock)

    store.set("k1", "v1", ttl_seconds=1)
    store.set("k2", "v2", ttl_seconds=2)
    store.set("k3", "v3", ttl_seconds=3)

    fake_clock.advance(2)

    # After advancing, test cleanup
    assert store.get("k1") is None
    assert store.get("k2") is None
    assert store.get("k3") == "v3"


def test_zero_and_negative_ttl_does_not_store(fake_clock):
    policy = ProactiveExpirationPolicy()
    store = Store(expiration_policy=policy, clock=fake_clock)

    store.set("n0", "none", ttl_seconds=0)
    store.set("n1", "none", ttl_seconds=-5)

    assert store.get("n0") is None
    assert store.get("n1") is None