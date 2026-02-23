import pytest

from src.store import Store
from src.expiration.on_demand import OnDemandExpirationPolicy
from src.expiration.proactive import ProactiveExpirationPolicy


@pytest.mark.parametrize("policy_class", [
    OnDemandExpirationPolicy,
    ProactiveExpirationPolicy,
])
def test_set_and_get(fake_clock, policy_class):
    policy = policy_class()
    store = Store(expiration_policy=policy, clock=fake_clock)

    store.set("foo", "bar", ttl_seconds=10)
    assert store.get("foo") == "bar"


@pytest.mark.parametrize("policy_class", [
    OnDemandExpirationPolicy,
    ProactiveExpirationPolicy,
])
def test_missing_key_returns_none(fake_clock, policy_class):
    policy = policy_class()
    store = Store(expiration_policy=policy, clock=fake_clock)

    assert store.get("missing") is None


@pytest.mark.parametrize("policy_class", [
    OnDemandExpirationPolicy,
    ProactiveExpirationPolicy,
])
def test_ttl_zero_negative(fake_clock, policy_class):
    policy = policy_class()
    store = Store(expiration_policy=policy, clock=fake_clock)

    store.set("k0", "v", ttl_seconds=0)
    store.set("k1", "v", ttl_seconds=-5)

    assert store.get("k0") is None
    assert store.get("k1") is None


@pytest.mark.parametrize("policy_class", [
    OnDemandExpirationPolicy,
    ProactiveExpirationPolicy,
])
def test_expiration_after_ttl(fake_clock, policy_class):
    policy = policy_class()
    store = Store(expiration_policy=policy, clock=fake_clock)

    store.set("key", "val", ttl_seconds=3)
    fake_clock.advance(4)

    # Once expired, should be None
    assert store.get("key") is None