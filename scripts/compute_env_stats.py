#!/usr/bin/env python3
"""
Parse a JUnit XML file produced by pytest and write a compact stats JSON.

Used by the unified nightly pipeline so MergeAndReport can build a
per-environment summary table in the consolidated email without having
to run allure generate once per environment.

Usage:
    python3 scripts/compute_env_stats.py \
        --junit-xml  reports/junit/qa1.xml \
        --env-name   qa1 \
        --output     reports/qa1-stats.json
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="JUnit XML -> stats JSON")
    p.add_argument("--junit-xml", required=True, help="Path to JUnit XML produced by pytest")
    p.add_argument("--env-name",  required=True, help="Environment label (qa1, stag, prod, china_prod, china_stag)")
    p.add_argument("--output",    required=True, help="Output JSON path")
    return p.parse_args()


def parse_junit(path: str) -> dict:
    """
    Parse a JUnit XML file and return raw counters.
    Handles both <testsuites> (multiple suites) and bare <testsuite> root.
    """
    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except Exception as exc:
        print(f"[WARN] Cannot parse JUnit XML at {path!r}: {exc}", file=sys.stderr)
        return {"total": 0, "failures": 0, "errors": 0, "skipped": 0}

    def _int(el, attr) -> int:
        try:
            return int(el.get(attr, 0))
        except (ValueError, TypeError):
            return 0

    if root.tag == "testsuites":
        suites = root.findall("testsuite")
    else:
        suites = [root]

    total    = sum(_int(s, "tests")    for s in suites)
    failures = sum(_int(s, "failures") for s in suites)
    errors   = sum(_int(s, "errors")   for s in suites)
    skipped  = sum(_int(s, "skipped")  for s in suites)

    return {"total": total, "failures": failures, "errors": errors, "skipped": skipped}


def compute_stats(env_name: str, raw: dict) -> dict:
    total    = raw["total"]
    failures = raw["failures"]
    errors   = raw["errors"]
    skipped  = raw["skipped"]
    failed   = failures + errors
    passed   = max(0, total - failed - skipped)

    pass_pct = round(passed / total * 100, 1) if total > 0 else 0.0

    return {
        "env":          env_name,
        "total":        total,
        "passed":       passed,
        "failed":       failed,
        "skipped":      skipped,
        "pass_pct":     pass_pct,
        "had_failures": failed > 0,
    }


def main() -> None:
    args  = parse_args()
    raw   = parse_junit(args.junit_xml)
    stats = compute_stats(args.env_name, raw)

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2)

    flag = " [FAILURES DETECTED]" if stats["had_failures"] else ""
    print(
        f"[OK] {args.env_name}: "
        f"{stats['passed']} passed / {stats['failed']} failed / "
        f"{stats['skipped']} skipped  ({stats['pass_pct']}%){flag}"
    )


if __name__ == "__main__":
    main()
