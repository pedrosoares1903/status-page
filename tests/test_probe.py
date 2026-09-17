"""The verdict rules. No network is touched here — that is the point."""

import pytest

from src.probe import classify


@pytest.mark.parametrize(
    ("code", "latency_ms", "expected"),
    [
        (200, 120, "ok"),
        (204, 10, "ok"),
        (301, 50, "down"),  # a redirect is not an outage
        (200, 1000, "slow"),  # exactly on the threshold counts as slow
        (200, 4200, "slow"),
        (404, 30, "down"),
        (500, 30, "down"),
        (None, 5000, "down"),  # timeout or connection refused
    ],
)
def test_classify(code, latency_ms, expected):
    assert classify(code, latency_ms) == expected


def test_threshold_is_configurable():
    assert classify(200, 300, slow_threshold_ms=200) == "slow"
    assert classify(200, 300, slow_threshold_ms=400) == "ok"
