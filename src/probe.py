"""Probe public endpoints and classify what came back.

The network call and the decision are deliberately kept apart:
`classify` is a pure function, so every rule can be tested without a network.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import UTC, datetime

import requests

SLOW_THRESHOLD_MS = 1000
DEFAULT_TIMEOUT_S = 5.0


@dataclass(frozen=True)
class Check:
    name: str
    url: str
    status: str  # "ok" | "slow" | "down"
    code: int | None
    latency_ms: int
    checked_at: str


def classify(
    code: int | None,
    latency_ms: int,
    slow_threshold_ms: int = SLOW_THRESHOLD_MS,
) -> str:
    """Turn an observation into a verdict. No network, no clock, no files."""
    if code is None or code >= 400:
        return "down"
    if latency_ms >= slow_threshold_ms:
        return "slow"
    return "ok"


def probe(name: str, url: str, timeout_s: float = DEFAULT_TIMEOUT_S) -> Check:
    """Make one request and report what happened. Never raises."""
    started = time.perf_counter()
    code: int | None = None
    try:
        code = requests.get(url, timeout=timeout_s).status_code
    except requests.RequestException:
        code = None
    latency_ms = int((time.perf_counter() - started) * 1000)

    return Check(
        name=name,
        url=url,
        status=classify(code, latency_ms),
        code=code,
        latency_ms=latency_ms,
        checked_at=datetime.now(UTC).isoformat(timespec="seconds"),
    )