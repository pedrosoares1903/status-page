"""The page is built from a pure function, so it can be asserted on."""

from src.probe import Check
from src.render import render

CHECKS = [
    Check("GitHub API", "https://api.github.com", "ok", 200, 143, "2026-09-17T10:00:00+00:00"),
    Check("Slow service", "https://example.com", "slow", 200, 2400, "2026-09-17T10:00:00+00:00"),
    Check("Broken <thing>", "https://example.org", "down", 503, 88, "2026-09-17T10:00:00+00:00"),
]


def test_every_target_appears():
    page = render(CHECKS, "2026-09-17 10:00 UTC")
    assert "GitHub API" in page
    assert "Slow service" in page


def test_status_labels_are_human_readable():
    page = render(CHECKS, "2026-09-17 10:00 UTC")
    assert "operational" in page
    assert "degraded" in page
    assert "down" in page


def test_names_are_escaped():
    page = render(CHECKS, "2026-09-17 10:00 UTC")
    assert "Broken &lt;thing&gt;" in page
    assert "<thing>" not in page