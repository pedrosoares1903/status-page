"""Turn a list of checks into a standalone HTML page. Pure function."""

from __future__ import annotations

from html import escape

from .probe import Check

COLOUR = {"ok": "#16a34a", "slow": "#d97706", "down": "#dc2626"}
LABEL = {"ok": "operational", "slow": "degraded", "down": "down"}

_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Service status</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 16px/1.5 system-ui, sans-serif; max-width: 42rem;
          margin: 3rem auto; padding: 0 1rem; }}
  h1 {{ font-size: 1.5rem; margin-bottom: .25rem; }}
  .sub {{ color: #6b7280; font-size: .875rem; margin-top: 0; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ display: flex; align-items: baseline; gap: .75rem;
        padding: .75rem 0; border-bottom: 1px solid #e5e7eb33; }}
  .dot {{ width: .625rem; height: .625rem; border-radius: 50%; flex: none; }}
  .name {{ flex: 1; }}
  .meta {{ color: #6b7280; font-size: .8125rem; font-variant-numeric: tabular-nums; }}
</style>
</head>
<body>
<h1>Service status</h1>
<p class="sub">Generated {generated_at} · checked from GitHub Actions</p>
<ul>
{rows}
</ul>
</body>
</html>
"""

_ROW = (
    '<li><span class="dot" style="background:{colour}"></span>'
    '<span class="name">{name}</span>'
    '<span class="meta">{label} · {latency} ms</span></li>'
)


def render(checks: list[Check], generated_at: str) -> str:
    rows = "\n".join(
        _ROW.format(
            colour=COLOUR[c.status],
            name=escape(c.name),
            label=escape(LABEL[c.status]),
            latency=c.latency_ms,
        )
        for c in checks
    )
    return _PAGE.format(generated_at=escape(generated_at), rows=rows)
