#!/usr/bin/env python3
"""
Fetch and analyze Azure DevOps pipeline failures.

Usage:
    python scripts/fetch_pipeline_failures.py --build-id 260518
    python scripts/fetch_pipeline_failures.py --build-id 260518 --show-body

Requires:
    AZURE_DEVOPS_PAT env var — Personal Access Token with 'Read' access to Build & Test

How to get a PAT:
    Azure DevOps → User Settings → Personal Access Tokens → New Token
    Scopes: Build (Read), Test Management (Read)
"""

import argparse
import base64
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ORG = "netafimdf"
PROJECT = "NetbeatVx"
BASE = f"https://dev.azure.com/{ORG}/{PROJECT}/_apis"


def auth_header(pat: str) -> dict:
    token = base64.b64encode(f":{pat}".encode()).decode()
    return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}


def get(url: str, headers: dict) -> dict:
    req = Request(url, headers=headers)
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def fetch_failed_tests(build_id: str, headers: dict) -> list[dict]:
    # Get test runs for this build
    runs_url = f"{BASE}/test/runs?buildIds={build_id}&api-version=6.0"
    runs = get(runs_url, headers).get("value", [])
    if not runs:
        return []

    failures = []
    for run in runs:
        run_id = run["id"]
        results_url = (
            f"{BASE}/test/runs/{run_id}/results"
            f"?outcomes=Failed&$top=200&api-version=6.0"
        )
        results = get(results_url, headers).get("value", [])
        for r in results:
            failures.append({
                "test": r.get("testCaseTitle", ""),
                "suite": r.get("testSuite", {}).get("name", ""),
                "error": r.get("errorMessage", "").strip(),
                "duration_s": round(r.get("durationInMs", 0) / 1000, 2),
            })
    return failures


def fetch_build_summary(build_id: str, headers: dict) -> dict:
    url = f"{BASE}/build/builds/{build_id}?api-version=6.0"
    b = get(url, headers)
    return {
        "number": b.get("buildNumber", ""),
        "status": b.get("status", ""),
        "result": b.get("result", ""),
        "branch": b.get("sourceBranch", "").replace("refs/heads/", ""),
        "started": b.get("startTime", "")[:19].replace("T", " "),
        "finished": b.get("finishTime", "")[:19].replace("T", " "),
        "url": b.get("_links", {}).get("web", {}).get("href", ""),
    }


def fetch_test_stats(build_id: str, headers: dict) -> dict:
    runs_url = f"{BASE}/test/runs?buildIds={build_id}&api-version=6.0"
    runs = get(runs_url, headers).get("value", [])
    passed = failed = skipped = 0
    for r in runs:
        passed += r.get("passedTests", 0)
        failed += r.get("failedTests", 0) + r.get("incompleteTests", 0)
        skipped += r.get("skippedTests", 0) + r.get("notApplicableTests", 0)
    total = passed + failed + skipped
    pct = round(passed / total * 100, 1) if total else 0
    return {"total": total, "passed": passed, "failed": failed, "skipped": skipped, "pct": pct}


def group_by_error(failures: list[dict]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for f in failures:
        key = f["error"][:200] if f["error"] else "Unknown error"
        groups.setdefault(key, []).append(f["test"])
    return dict(sorted(groups.items(), key=lambda x: -len(x[1])))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-id", required=True)
    parser.add_argument("--show-body", action="store_true", help="Show full error messages")
    parser.add_argument("--top", type=int, default=5, help="Show top N error groups")
    args = parser.parse_args()

    pat = os.environ.get("AZURE_DEVOPS_PAT")
    if not pat:
        print("[ERROR] Set AZURE_DEVOPS_PAT environment variable.")
        sys.exit(1)

    headers = auth_header(pat)

    print(f"\n{'='*60}")
    print(f"  Pipeline Analysis — Build {args.build_id}")
    print(f"{'='*60}\n")

    try:
        summary = fetch_build_summary(args.build_id, headers)
        print(f"  Build   : {summary['number']}")
        print(f"  Branch  : {summary['branch']}")
        print(f"  Result  : {summary['result'].upper()}")
        print(f"  Started : {summary['started']}")
        print(f"  URL     : {summary['url']}\n")
    except Exception as e:
        print(f"[WARN] Could not fetch build summary: {e}\n")

    try:
        stats = fetch_test_stats(args.build_id, headers)
        print(f"  Tests   : {stats['total']} total")
        print(f"  Passed  : {stats['passed']}  ({stats['pct']}%)")
        print(f"  Failed  : {stats['failed']}")
        print(f"  Skipped : {stats['skipped']}\n")
    except Exception as e:
        print(f"[WARN] Could not fetch test stats: {e}\n")

    print(f"{'='*60}")
    print(f"  Top Failure Groups")
    print(f"{'='*60}\n")

    try:
        failures = fetch_failed_tests(args.build_id, headers)
        if not failures:
            print("  No test failures found.\n")
            return

        groups = group_by_error(failures)
        for i, (error, tests) in enumerate(list(groups.items())[:args.top], 1):
            print(f"  [{i}] {len(tests)} tests — {error[:120]}")
            for t in tests[:5]:
                print(f"       • {t}")
            if len(tests) > 5:
                print(f"       ... and {len(tests) - 5} more")
            print()

        if len(groups) > args.top:
            print(f"  ... and {len(groups) - args.top} more error groups (use --top N to see more)\n")

    except HTTPError as e:
        print(f"[ERROR] Azure DevOps API error: {e.code} {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
