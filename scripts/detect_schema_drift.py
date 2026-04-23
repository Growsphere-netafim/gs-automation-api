#!/usr/bin/env python3
"""
Detect OpenAPI schema drift between live services and the committed
swagger_specs/ baseline.

Used by the nightly pipeline to surface, in the email report, any
endpoint that was ADDED, REMOVED, or had its signature CHANGED since
the last time someone regenerated the baseline with
fetch_swagger_specs.py.

This script does NOT update the baseline — drift is only surfaced so
developers can regenerate and commit intentionally.

Usage:
    python3 scripts/detect_schema_drift.py \
        --specs-dir  swagger_specs \
        --output     reports/schema-drift.json

Environment:
    Reads swagger URLs from fetch_swagger_specs.URLS.

Exit code: always 0 — drift is informational, not a build failure.
"""

import argparse
import asyncio
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import aiohttp


# Re-use the URL list the project already maintains.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from fetch_swagger_specs import URLS, safe_filename_from_url  # type: ignore
except Exception as exc:  # pragma: no cover
    print(f"[ERROR] Cannot import fetch_swagger_specs: {exc}", file=sys.stderr)
    sys.exit(0)

TIMEOUT_SECONDS = 20
CONCURRENCY = 8


# ─────────────────────────────────────────────────────────────────────────────
# Fetch
# ─────────────────────────────────────────────────────────────────────────────


async def _fetch_one(session: aiohttp.ClientSession, sem: asyncio.Semaphore,
                     url: str) -> Tuple[str, Optional[dict], Optional[str]]:
    async with sem:
        try:
            async with session.get(url, ssl=False) as resp:
                if resp.status != 200:
                    return url, None, f"HTTP {resp.status}"
                text = await resp.text()
                return url, json.loads(text), None
        except Exception as exc:
            return url, None, f"{type(exc).__name__}: {exc}"


async def fetch_all_live() -> Tuple[Dict[str, dict], List[Tuple[str, str]]]:
    """Fetch every URL in URLS.
    Return:
      (live_specs, failed_urls)
      live_specs   = {host_filename -> spec_dict} for 200 responses
      failed_urls  = [(url, reason), ...] for everything that did not respond 200
    """
    timeout = aiohttp.ClientTimeout(total=TIMEOUT_SECONDS)
    sem = asyncio.Semaphore(CONCURRENCY)
    headers = {"Accept": "application/json"}
    live: Dict[str, dict] = {}
    failed: List[Tuple[str, str]] = []

    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        tasks = [_fetch_one(session, sem, url) for url in URLS]
        for url, spec, err in await asyncio.gather(*tasks):
            if err is not None:
                print(f"[WARN] Cannot fetch {url}: {err}", file=sys.stderr)
                failed.append((url, err))
                continue
            live[safe_filename_from_url(url)] = spec
    return live, failed


# ─────────────────────────────────────────────────────────────────────────────
# Migration candidate discovery
# ─────────────────────────────────────────────────────────────────────────────
#
# When a configured URL stops responding, try to find where the service moved
# by probing a small set of candidate hostnames that follow the patterns
# observed in this org's Azure -> Kubernetes migrations.
#
# Patterns observed:
#   qa1-netbeatvx-<svc>-app-weu.azurewebsites.net  ->  <svc>-qa1.k8s.growsphere.netafim.com
#   app-netbeatvx-<svc>-qa1.azurewebsites.net       ->  <svc>-qa1.k8s.growsphere.netafim.com
#
# Swagger path sometimes flips from /swagger/v1/swagger.json to /swagger/v2/swagger.json
# (TimeSeries was the precedent), so we try both when guessing a new URL.


_K8S_TEMPLATE   = "https://{svc}-qa1.k8s.growsphere.netafim.com{path}"
_SWAGGER_PATHS  = ("/swagger/v1/swagger.json", "/swagger/v2/swagger.json")

_OLD_PATTERNS = (
    # Azure Web App pattern A: qa1-netbeatvx-<svc>-app-weu.azurewebsites.net
    re.compile(r"^qa1-netbeatvx-(?P<svc>[a-z0-9-]+?)-app-weu\.azurewebsites\.net$"),
    # Azure Web App pattern B: app-netbeatvx-<svc>-qa1.azurewebsites.net
    re.compile(r"^app-netbeatvx-(?P<svc>[a-z0-9-]+?)-qa1\.azurewebsites\.net$"),
)


def _candidate_urls_for_old_host(host: str) -> List[str]:
    for rx in _OLD_PATTERNS:
        m = rx.match(host)
        if not m:
            continue
        svc = m.group("svc")
        return [_K8S_TEMPLATE.format(svc=svc, path=p) for p in _SWAGGER_PATHS]
    return []


async def _probe(session: aiohttp.ClientSession, url: str) -> Tuple[str, int]:
    try:
        async with session.get(url, ssl=False) as resp:
            return url, resp.status
    except Exception:
        return url, 0


async def find_migration_candidates(failed_urls: List[Tuple[str, str]]) -> List[dict]:
    """For each failed URL, probe likely new hostnames; return suggestions."""
    if not failed_urls:
        return []

    suggestions: List[dict] = []
    timeout = aiohttp.ClientTimeout(total=TIMEOUT_SECONDS)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        for url, err in failed_urls:
            host = urlparse(url).netloc
            candidates = _candidate_urls_for_old_host(host)
            if not candidates:
                continue
            # Probe each candidate
            results = await asyncio.gather(*(_probe(session, c) for c in candidates))
            hit = next((c for c, status in results if status == 200), None)
            if hit:
                suggestions.append({
                    "old_host":      host,
                    "old_reason":    err,
                    "new_candidate": hit,
                })
    return suggestions


# ─────────────────────────────────────────────────────────────────────────────
# Spec comparison
# ─────────────────────────────────────────────────────────────────────────────


def _op_signature(op: dict) -> str:
    """Stable hash of the parts of an operation that typically matter for
    test breakage: parameters (name+in+required), requestBody schema ref,
    response status codes.

    Ignores volatile bits like descriptions and summaries.
    """
    parts = []

    # Parameters: [(name, in, required)]
    for p in op.get("parameters") or []:
        parts.append(("param", p.get("name"), p.get("in"), bool(p.get("required", False))))

    # Request body: present / content-types
    rb = op.get("requestBody")
    if rb:
        content = rb.get("content") or {}
        parts.append(("requestBody", sorted(content.keys()), bool(rb.get("required", False))))

    # Responses: the set of status codes defined
    parts.append(("responses", sorted((op.get("responses") or {}).keys())))

    payload = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _extract_endpoints(spec: dict) -> Dict[Tuple[str, str], dict]:
    """Return {(method, path) -> operation_object}."""
    out: Dict[Tuple[str, str], dict] = {}
    for path, methods in (spec.get("paths") or {}).items():
        if not isinstance(methods, dict):
            continue
        for method, op in methods.items():
            if method.lower() in {"get", "post", "put", "patch", "delete", "head", "options"}:
                if isinstance(op, dict):
                    out[(method.upper(), path)] = op
    return out


def diff_spec(baseline: dict, live: dict) -> dict:
    """Return a dict with added/removed/changed endpoints between baseline and live."""
    baseline_eps = _extract_endpoints(baseline)
    live_eps = _extract_endpoints(live)

    baseline_keys = set(baseline_eps.keys())
    live_keys = set(live_eps.keys())

    added = sorted(live_keys - baseline_keys)
    removed = sorted(baseline_keys - live_keys)

    changed = []
    for key in sorted(baseline_keys & live_keys):
        if _op_signature(baseline_eps[key]) != _op_signature(live_eps[key]):
            changed.append(key)

    def _fmt(keys):
        return [{"method": m, "path": p} for (m, p) in keys]

    return {
        "added":   _fmt(added),
        "removed": _fmt(removed),
        "changed": _fmt(changed),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="OpenAPI schema drift detector")
    p.add_argument("--specs-dir", required=True, help="Baseline swagger_specs/ directory")
    p.add_argument("--output",    required=True, help="Path for the drift JSON report")
    return p.parse_args()


def _service_name_from_host(host_filename: str) -> str:
    # "csapi-qa1.k8s.growsphere.netafim.com.json" -> "csapi"
    return host_filename.split("-", 1)[0].replace(".json", "")


def main() -> None:
    args = parse_args()
    specs_dir = Path(args.specs_dir)
    if not specs_dir.is_dir():
        print(f"[WARN] specs dir {specs_dir} missing; emitting empty drift report.",
              file=sys.stderr)
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps({
            "generated_at": None,
            "services": [],
            "summary": {"added": 0, "removed": 0, "changed": 0, "services_with_drift": 0},
        }, indent=2))
        return

    live, failed_urls = asyncio.run(fetch_all_live())
    migration_suggestions = asyncio.run(find_migration_candidates(failed_urls))

    report_services: List[dict] = []
    total_added = total_removed = total_changed = 0

    for host_filename, live_spec in sorted(live.items()):
        baseline_path = specs_dir / host_filename
        if not baseline_path.is_file():
            # Service is brand new — treat every endpoint as 'added'
            live_keys = _extract_endpoints(live_spec)
            diff = {
                "added":   [{"method": m, "path": p} for (m, p) in sorted(live_keys.keys())],
                "removed": [],
                "changed": [],
            }
        else:
            try:
                baseline_spec = json.loads(baseline_path.read_text("utf-8"))
            except Exception as exc:
                print(f"[WARN] Cannot parse baseline {baseline_path}: {exc}", file=sys.stderr)
                continue
            diff = diff_spec(baseline_spec, live_spec)

        if diff["added"] or diff["removed"] or diff["changed"]:
            report_services.append({
                "host":    host_filename.replace(".json", ""),
                "service": _service_name_from_host(host_filename),
                **diff,
            })
            total_added   += len(diff["added"])
            total_removed += len(diff["removed"])
            total_changed += len(diff["changed"])

    # Also flag baseline files with NO live response (service went offline /
    # URL changed). We don't list endpoint-level removals here — just the host.
    offline_services: List[str] = []
    for baseline_file in sorted(specs_dir.glob("*.json")):
        if baseline_file.name not in live:
            offline_services.append(baseline_file.name.replace(".json", ""))

    from datetime import datetime, timezone
    report = {
        "generated_at":          datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "services":              report_services,
        "offline":               offline_services,
        "migration_suggestions": migration_suggestions,
        "summary": {
            "added":                 total_added,
            "removed":               total_removed,
            "changed":               total_changed,
            "services_with_drift":   len(report_services),
            "services_offline":      len(offline_services),
            "migration_suggestions": len(migration_suggestions),
        },
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")

    s = report["summary"]
    print(
        f"[OK] Schema drift: {s['added']} added / {s['removed']} removed / "
        f"{s['changed']} changed across {s['services_with_drift']} services. "
        f"{s['services_offline']} services unreachable. "
        f"{s['migration_suggestions']} migration suggestion(s)."
    )


if __name__ == "__main__":
    main()
