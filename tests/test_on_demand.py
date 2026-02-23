import time

import pytest

from src.expiration.on_demand import OnDemandExpirationPolicy
from src.store import Store




def test_set_and_get_not_expired(fake_clock):
    policy = OnDemandExpirationPolicy()
    store = Store(expiration_policy=policy, clock=fake_clock)

    store.set("a", "value", ttl_seconds=5)
    assert store.get("a") == "value"


def test_get_expired_on_demand(fake_clock):
    policy = OnDemandExpirationPolicy()
    store = Store(expiration_policy=policy, clock=fake_clock)

    store.set("key", "v", ttl_seconds=2)
    fake_clock.advance(3)

    # expired, cleanup should delete it
    assert store.get("key") is None


def test_missing_key_returns_none(fake_clock):
    policy = OnDemandExpirationPolicy()
    store = Store(expiration_policy=policy, clock=fake_clock)

    assert store.get("nope") is None


def test_ttl_zero_or_negative_causes_no_store(fake_clock):
    policy = OnDemandExpirationPolicy()
    store = Store(expiration_policy=policy, clock=fake_clock)

    store.set("x", "y", ttl_seconds=0)
    assert store.get("x") is None

    store.set("z", "y", ttl_seconds=-5)
    assert store.get("z") is None