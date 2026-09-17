"""Read the target list, probe every entry, write public/index.html."""

from __future__ import annotations

import pathlib
from datetime import UTC, datetime

import yaml

from src.probe import probe
from src.render import render

ROOT = pathlib.Path(__file__).parent
OUTPUT = ROOT / "public" / "index.html"


def main() -> None:
    targets = yaml.safe_load((ROOT / "targets.yml").read_text())["targets"]
    checks = [probe(t["name"], t["url"]) for t in targets]

    for c in checks:
        print(f"{c.status:>4}  {c.latency_ms:>5} ms  {c.name}")

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(render(checks, datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")))
    print(f"\nwrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
