import pytest


class FakeClock:
    def __init__(self, start: int):
        self.now = start

    def advance(self, seconds: int) -> None:
        self.now += seconds

    def __call__(self) -> int:
        return self.now


@pytest.fixture
def fake_clock():
    """
    Provides a fresh FakeClock instance for tests.
    """
    # default start time can be anything — override in test if needed
    return FakeClock(start=100)