"""Generates the AGENT CONSOLE SVG banner from live GitHub activity.

Run by .github/workflows/agent-console.yml on a schedule. Renders
assets/console.svg. Falls back to static placeholder data if the API is
unreachable so a transient network or rate-limit failure never breaks the
profile image.

Two auth modes:
- PROFILE_TOKEN set (a personal access token with repo read access): sees
  the real account, including private repos, so repo/star counts and the
  contribution total match what's shown on the GitHub profile page.
- PROFILE_TOKEN absent: falls back to the public, unauthenticated API,
  which only sees public repos and undercounts real activity.

Either way, private repo NAMES are never written into the SVG -- only
aggregate numbers (counts, dates) and public repo names, matching exactly
what GitHub already shows publicly on the profile's contribution graph and
repo counter. See private repos only feed aggregate stats, anonymized as
"[TASK] private repo synced" in the task log.
"""

from __future__ import annotations

import html
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

USERNAME = os.environ.get("GH_USERNAME", "mohamedmeksi")
PROFILE_TOKEN = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN")
HAS_OWNER_ACCESS = bool(os.environ.get("PROFILE_TOKEN"))
API_ROOT = "https://api.github.com"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "assets" / "console.svg"

FALLBACK = {
    "repos": 0,
    "stars": 0,
    "contributions_1y": 0,
    "last_deploy": "n/a",
    "tasks": ["[AGENT] no signal · waiting for first sync"],
}


@dataclass
class ConsoleData:
    repos: int
    stars: int
    contributions_1y: int | None
    last_deploy: str
    tasks: list[str] = field(default_factory=list)


def _fetch(path: str) -> object:
    request = urllib.request.Request(
        f"{API_ROOT}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": USERNAME,
            **({"Authorization": f"Bearer {PROFILE_TOKEN}"} if PROFILE_TOKEN else {}),
        },
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read())


def _graphql(query: str, variables: dict) -> dict | None:
    """Returns None on any failure -- a broken query must never crash the run."""
    if not PROFILE_TOKEN:
        return None
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        f"{API_ROOT}/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {PROFILE_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": USERNAME,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.loads(response.read())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return None
    return payload.get("data")


def _hours_since(iso_timestamp: str) -> int:
    dt = datetime.strptime(iso_timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return int((datetime.now(timezone.utc) - dt).total_seconds() // 3600)


def _fetch_contributions_1y() -> int | None:
    if not HAS_OWNER_ACCESS:
        return None
    data = _graphql(
        "query { viewer { contributionsCollection { contributionCalendar { totalContributions } } } }",
        {},
    )
    try:
        return data["viewer"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    except (TypeError, KeyError):
        return None


def collect_data() -> ConsoleData:
    """Pull live stats. Any API failure returns FALLBACK instead of raising,
    so a bad run never leaves the profile without an image."""
    try:
        if HAS_OWNER_ACCESS:
            # Authenticated as the account owner: sees private repos too,
            # so counts match what the GitHub profile page itself shows.
            repos = _fetch("/user/repos?per_page=100&sort=pushed&affiliation=owner")
        else:
            # Public API only -- undercounts real activity, but works with
            # zero setup (default Actions token, no secret required).
            repos = _fetch(f"/users/{USERNAME}/repos?per_page=100&sort=pushed")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return ConsoleData(**FALLBACK)

    if not isinstance(repos, list):
        return ConsoleData(**FALLBACK)

    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    contributions_1y = _fetch_contributions_1y()

    if repos and repos[0].get("pushed_at"):
        hours_ago = _hours_since(repos[0]["pushed_at"])
        last_deploy = f"{hours_ago}h ago" if hours_ago < 48 else f"{hours_ago // 24}d ago"
    else:
        last_deploy = "n/a"

    # Task log: never print a private repo's name -- that would leak
    # project/client info a public profile has no business exposing. Public
    # repos are named as usual; private ones show up anonymized so recent
    # activity still reads as "alive" instead of falsely idle.
    tasks: list[str] = []
    for repo in repos[:4]:
        if not repo.get("pushed_at"):
            continue
        recency_hours = _hours_since(repo["pushed_at"])
        recency = f"{recency_hours}h ago" if recency_hours < 48 else f"{recency_hours // 24}d ago"
        if repo.get("private"):
            tasks.append(f"[TASK] private repo synced · {recency}")
        else:
            tasks.append(f"[TASK] {repo['name']} last synced · {recency}")

    if not tasks:
        tasks = ["[AGENT] no signal · active work continues on private/client repos"]

    return ConsoleData(
        repos=len(repos),
        stars=total_stars,
        contributions_1y=contributions_1y,
        last_deploy=last_deploy,
        tasks=tasks,
    )


def render_svg(data: ConsoleData) -> str:
    width, height = 820, 380
    line_height = 23
    log_start_y = 236
    n_tasks = min(len(data.tasks), 4)
    contributions_display = str(data.contributions_1y) if data.contributions_1y is not None else "n/a"

    log_rows = "".join(
        f'<text x="40" y="{log_start_y + i * line_height}" class="log" opacity="0">'
        f'{html.escape(task)}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{1.0 + i * 0.3:.1f}s" dur="0.25s" fill="freeze"/>'
        f"</text>"
        for i, task in enumerate(data.tasks[:4])
    )
    cursor_begin = 1.0 + n_tasks * 0.3 + 0.2
    cursor_y = log_start_y + n_tasks * line_height

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Agent console status panel, live status and task log for Mohamed Meksi">
  <defs>
    <radialGradient id="bgGlow" cx="30%" cy="0%" r="80%">
      <stop offset="0%" stop-color="#1f6feb" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0"/>
    </radialGradient>
    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <style>
      .bg {{ fill: #0d1117; }}
      .panel {{ fill: #161b22; stroke: #388bfd; stroke-opacity: 0.5; stroke-width: 1; }}
      .title {{ font: 700 20px 'Fira Code', 'Cascadia Code', monospace; fill: #58a6ff; letter-spacing: 1px; }}
      .status {{ font: 600 13px 'Fira Code', 'Cascadia Code', monospace; fill: #3fb950; }}
      .connecting {{ font: 600 13px 'Fira Code', 'Cascadia Code', monospace; fill: #d29922; }}
      .label {{ font: 400 13px 'Fira Code', 'Cascadia Code', monospace; fill: #8b949e; }}
      .value {{ font: 600 13px 'Fira Code', 'Cascadia Code', monospace; fill: #e6edf3; }}
      .log {{ font: 400 12px 'Fira Code', 'Cascadia Code', monospace; fill: #79c0ff; }}
      .dim {{ font: 400 11px 'Fira Code', 'Cascadia Code', monospace; fill: #6e7681; }}
      .cursor {{ fill: #79c0ff; }}
    </style>
  </defs>

  <rect class="bg" width="{width}" height="{height}" rx="10"/>
  <rect width="{width}" height="{height}" rx="10" fill="url(#bgGlow)"/>
  <rect class="panel" x="12" y="12" width="{width - 24}" height="{height - 24}" rx="8">
    <animate attributeName="stroke-opacity" values="0.25;0.6;0.25" dur="3.5s" repeatCount="indefinite"/>
  </rect>

  <circle cx="34" cy="34" r="5" fill="#ff5f56"/>
  <circle cx="52" cy="34" r="5" fill="#ffbd2e"/>
  <circle cx="70" cy="34" r="5" fill="#27c93f"/>
  <text x="90" y="39" class="dim">agent://mohamed-meksi/console</text>

  <text x="40" y="84" class="title" filter="url(#softGlow)" opacity="0">
    AGENT: MEK
    <animate attributeName="opacity" from="0" to="1" begin="0s" dur="0.5s" fill="freeze"/>
  </text>

  <text x="240" y="84" class="connecting">
    ◌ CONNECTING...
    <animate attributeName="opacity" from="1" to="0" begin="0.1s" dur="0.7s" fill="freeze"/>
  </text>
  <text x="240" y="84" class="status" opacity="0">
    ● STATUS: ONLINE
    <animate attributeName="opacity" from="0" to="1" begin="0.75s" dur="0.3s" fill="freeze"/>
    <animate attributeName="opacity" values="1;0.55;1" dur="2.4s" begin="1.1s" repeatCount="indefinite"/>
  </text>

  <text x="470" y="84" class="dim">OPERATOR: Mohamed Meksi</text>

  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="0.5s" dur="0.5s" fill="freeze"/>

    <text x="40" y="118" class="label">MISSION:</text>
    <text x="130" y="118" class="value">WhatsApp &amp; AI agent · full-stack developer</text>

    <line x1="40" y1="136" x2="{width - 40}" y2="136" stroke="#30363d" stroke-width="1"/>

    <text x="40" y="164" class="label">repos_shipped</text>
    <text x="190" y="164" class="value">{data.repos}</text>

    <text x="280" y="164" class="label">stars_earned</text>
    <text x="430" y="164" class="value">{data.stars}</text>

    <text x="510" y="164" class="label">contributions_1y</text>
    <text x="660" y="164" class="value">{contributions_display}</text>

    <text x="40" y="192" class="label">last_public_push</text>
    <text x="190" y="192" class="value">{html.escape(data.last_deploy)}</text>

    <line x1="40" y1="210" x2="{width - 40}" y2="210" stroke="#30363d" stroke-width="1"/>

    <text x="40" y="{log_start_y - 16}" class="label">$ tail -f task_queue.log</text>
  </g>

  {log_rows}

  <rect class="cursor" x="40" y="{cursor_y - 10}" width="8" height="13" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{cursor_begin:.1f}s" dur="0.15s" fill="freeze"/>
    <animate attributeName="opacity" values="1;0;1" dur="1s" begin="{cursor_begin + 0.15:.1f}s" repeatCount="indefinite"/>
  </rect>
</svg>"""


def main() -> None:
    data = collect_data()
    svg = render_svg(data)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(svg, encoding="utf-8")
    print(f"wrote {OUTPUT_PATH} for user={USERNAME} repos={data.repos} stars={data.stars}")


if __name__ == "__main__":
    main()
