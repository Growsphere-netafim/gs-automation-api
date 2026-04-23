#!/usr/bin/env python3
"""
Send one consolidated HTML nightly-report email covering all environments.

Called from pipelines/nightly-all-envs.yml after MergeAndReport generates
the combined Allure report.

Usage:
    python3 scripts/send_combined_report_email.py \
        --env-stats   reports/qa1-stats.json \
                      reports/stag-stats.json \
                      reports/prod-stats.json \
                      reports/china_prod-stats.json \
                      reports/china_stag-stats.json \
        --build-id    "$(Build.BuildId)" \
        --build-number "$(Build.BuildNumber)" \
        --report-url  "https://..." \
        --recipients  "a@x.com, b@x.com"

Required environment variables:
    SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, NOREPLY_EMAIL
"""

import argparse
import json
import os
import smtplib
import ssl
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Multi-env consolidated nightly email")
    p.add_argument("--env-stats",    nargs="+", required=True,
                   help="One or more paths to per-env stats JSON files")
    p.add_argument("--build-id",     default="0")
    p.add_argument("--build-number", default="")
    p.add_argument("--report-url",   default="")
    p.add_argument("--recipients",   required=True)
    return p.parse_args()


# ─────────────────────────────────────────────────────────────────────────────
# Stats loading
# ─────────────────────────────────────────────────────────────────────────────

_EMPTY_STATS = {
    "env": "unknown", "total": 0, "passed": 0,
    "failed": 0, "skipped": 0, "xfailed": 0, "pass_pct": 0.0, "had_failures": False,
}


def load_env_stats(paths: list[str]) -> list[dict]:
    results = []
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            # Backfill xfailed for older stats files
            data.setdefault("xfailed", 0)
            results.append(data)
        except Exception as exc:
            print(f"[WARN] Cannot read stats file {path!r}: {exc}", file=sys.stderr)
            results.append({**_EMPTY_STATS, "env": Path(path).stem.replace("-stats", "")})
    return results


def aggregate(envs: list[dict]) -> dict:
    total   = sum(e["total"]   for e in envs)
    passed  = sum(e["passed"]  for e in envs)
    failed  = sum(e["failed"]  for e in envs)
    skipped = sum(e["skipped"] for e in envs)
    xfailed = sum(e.get("xfailed", 0) for e in envs)
    pass_pct = round(passed / total * 100, 1) if total > 0 else 0.0

    pass_width = int(round(passed / total * 100)) if total > 0 else 0
    fail_width = int(round(failed / total * 100)) if total > 0 else 0
    # guarantee at least 1px width when non-zero
    if passed > 0 and pass_width == 0:
        pass_width = 1
    if failed > 0 and fail_width == 0:
        fail_width = 1

    return dict(
        total=total, passed=passed, failed=failed, skipped=skipped, xfailed=xfailed,
        pass_pct=pass_pct, pass_width=pass_width, fail_width=fail_width,
        any_failure=any(e["had_failures"] for e in envs),
    )


# ─────────────────────────────────────────────────────────────────────────────
# HTML generation
# ─────────────────────────────────────────────────────────────────────────────

_ENV_ORDER = ["qa1", "stag", "prod", "china_prod", "china_stag"]

_ENV_LABEL = {
    "qa1":        "QA1",
    "stag":       "STAG",
    "prod":       "PROD",
    "china_prod": "CHINA PROD",
    "china_stag": "CHINA STAG",
}

_ENV_COLOR = {
    "qa1":        "#5dade2",   # sky blue
    "stag":       "#af7ac5",   # violet
    "prod":       "#2ecc71",   # emerald
    "china_prod": "#e67e22",   # amber
    "china_stag": "#d35400",   # dark orange
}


def _status_badge(env_data: dict) -> str:
    if env_data["total"] == 0:
        return '<span style="background:#5d6d7e;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;">NO DATA</span>'
    if env_data["had_failures"]:
        return '<span style="background:#c0392b;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;">FAILED</span>'
    return '<span style="background:#1e8449;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;">PASSED</span>'


def _env_rows(envs: list[dict]) -> str:
    # Sort by canonical execution order
    env_map = {e["env"]: e for e in envs}
    ordered = [env_map[k] for k in _ENV_ORDER if k in env_map]
    # Append any extra envs not in _ENV_ORDER
    known = set(_ENV_ORDER)
    for e in envs:
        if e["env"] not in known:
            ordered.append(e)

    rows = []
    for e in ordered:
        env_key   = e["env"]
        label     = _ENV_LABEL.get(env_key, env_key.upper())
        color     = _ENV_COLOR.get(env_key, "#7f8fa4")
        badge     = _status_badge(e)
        pass_pct  = e["pass_pct"]
        total     = e["total"]
        passed    = e["passed"]
        failed    = e["failed"]
        skipped   = e["skipped"]
        xfailed   = e.get("xfailed", 0)

        rows.append(f"""
          <tr>
            <td style="padding:10px 12px; border-bottom:1px solid #2c3e50;">
              <span style="color:{color}; font-weight:600; font-size:13px;">{label}</span>
            </td>
            <td style="padding:10px 12px; border-bottom:1px solid #2c3e50; text-align:center;">{badge}</td>
            <td style="padding:10px 12px; border-bottom:1px solid #2c3e50; text-align:center; color:#ecf0f1;">{total}</td>
            <td style="padding:10px 12px; border-bottom:1px solid #2c3e50; text-align:center; color:#2ecc71; font-weight:600;">{passed}</td>
            <td style="padding:10px 12px; border-bottom:1px solid #2c3e50; text-align:center; color:#e74c3c; font-weight:600;">{failed}</td>
            <td style="padding:10px 12px; border-bottom:1px solid #2c3e50; text-align:center; color:#85929e;">{skipped}</td>
            <td style="padding:10px 12px; border-bottom:1px solid #2c3e50; text-align:center; color:#f39c12; font-weight:600;">{xfailed}</td>
            <td style="padding:10px 12px; border-bottom:1px solid #2c3e50; text-align:center; color:#ecf0f1;">{pass_pct}%</td>
          </tr>""")

    return "\n".join(rows)


def build_html(
    envs: list[dict],
    agg: dict,
    build_id: str,
    build_number: str,
    report_url: str,
) -> str:
    total      = agg["total"]
    passed     = agg["passed"]
    failed     = agg["failed"]
    skipped    = agg["skipped"]
    xfailed    = agg.get("xfailed", 0)
    pass_pct   = agg["pass_pct"]
    pass_width = agg["pass_width"]
    fail_width = agg["fail_width"]

    overall_color = "#c0392b" if agg["any_failure"] else "#1e8449"
    overall_label = "FAILURES DETECTED" if agg["any_failure"] else "ALL PASSED"

    env_rows_html = _env_rows(envs)

    return f"""<div style="font-family:'Segoe UI',Arial,sans-serif;background-color:#0f1923;padding:28px;">
  <div style="background-color:#1b2838;max-width:680px;margin:0 auto;border-radius:10px;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,0.5);">

    <!-- Header -->
    <div style="background:linear-gradient(135deg,#1b2a3b 0%,#2c3e50 100%);padding:24px 20px;text-align:center;">
      <p style="color:#5dade2;margin:0 0 6px 0;font-size:11px;text-transform:uppercase;letter-spacing:3px;">API Automation - All Environments</p>
      <h2 style="color:#ffffff;margin:0;font-weight:600;font-size:22px;letter-spacing:0.5px;">Nightly Test Report</h2>
      <p style="color:#85929e;margin:8px 0 0 0;font-size:13px;">qa1 &rarr; stag &rarr; prod &rarr; china prod &rarr; china stag</p>
      <div style="margin-top:10px;">
        <span style="background:{overall_color};color:#fff;padding:3px 12px;border-radius:12px;font-size:12px;font-weight:700;letter-spacing:1px;">{overall_label}</span>
      </div>
    </div>

    <div style="padding:32px 28px;">

      <!-- Overall pass % -->
      <div style="text-align:center;margin-bottom:24px;">
        <h1 style="font-size:52px;color:#ffffff;margin:0;font-weight:700;letter-spacing:-1px;">{pass_pct}%</h1>
        <span style="color:#7f8fa4;font-size:13px;text-transform:uppercase;letter-spacing:2px;">Overall Success Rate</span>
      </div>

      <!-- Progress bar -->
      <div style="height:10px;background-color:#253545;border-radius:5px;overflow:hidden;display:flex;margin-bottom:28px;">
        <div style="width:{pass_width}%;background:linear-gradient(90deg,#27ae60,#2ecc71);"></div>
        <div style="width:{fail_width}%;background:linear-gradient(90deg,#c0392b,#e74c3c);"></div>
      </div>

      <!-- Overall stats row -->
      <table style="width:100%;border-collapse:separate;border-spacing:8px;margin-bottom:28px;">
        <tr>
          <td style="background:#253545;padding:14px 10px;border-radius:8px;text-align:center;border-bottom:3px solid #3d5166;">
            <div style="font-size:24px;font-weight:700;color:#ecf0f1;">{total}</div>
            <div style="font-size:11px;color:#7f8fa4;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Total</div>
          </td>
          <td style="background:#1a3a2a;padding:14px 10px;border-radius:8px;text-align:center;border-bottom:3px solid #2ecc71;">
            <div style="font-size:24px;font-weight:700;color:#2ecc71;">{passed}</div>
            <div style="font-size:11px;color:#58d68d;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Passed</div>
          </td>
          <td style="background:#3a1a1a;padding:14px 10px;border-radius:8px;text-align:center;border-bottom:3px solid #e74c3c;">
            <div style="font-size:24px;font-weight:700;color:#e74c3c;">{failed}</div>
            <div style="font-size:11px;color:#ec7063;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Failed</div>
          </td>
          <td style="background:#253545;padding:14px 10px;border-radius:8px;text-align:center;border-bottom:3px solid #5d6d7e;">
            <div style="font-size:24px;font-weight:700;color:#85929e;">{skipped}</div>
            <div style="font-size:11px;color:#7f8fa4;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Skipped</div>
          </td>
          <td style="background:#3a2d14;padding:14px 10px;border-radius:8px;text-align:center;border-bottom:3px solid #f39c12;">
            <div style="font-size:24px;font-weight:700;color:#f39c12;" title="Known backend bugs — if this drops, a bug was fixed">{xfailed}</div>
            <div style="font-size:11px;color:#f39c12;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Known Bugs</div>
          </td>
        </tr>
      </table>

      <!-- Per-environment breakdown -->
      <div style="background:#1e2b37;border-radius:8px;overflow:hidden;margin-bottom:28px;">
        <div style="padding:12px 16px;background:#253545;border-bottom:1px solid #2c3e50;">
          <span style="color:#5dade2;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:2px;">Per-Environment Breakdown</span>
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:13px;">
          <thead>
            <tr style="background:#1b2838;">
              <th style="padding:8px 12px;text-align:left;color:#7f8fa4;font-weight:400;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Environment</th>
              <th style="padding:8px 12px;text-align:center;color:#7f8fa4;font-weight:400;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Status</th>
              <th style="padding:8px 12px;text-align:center;color:#7f8fa4;font-weight:400;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Total</th>
              <th style="padding:8px 12px;text-align:center;color:#7f8fa4;font-weight:400;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Passed</th>
              <th style="padding:8px 12px;text-align:center;color:#7f8fa4;font-weight:400;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Failed</th>
              <th style="padding:8px 12px;text-align:center;color:#7f8fa4;font-weight:400;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Skipped</th>
              <th style="padding:8px 12px;text-align:center;color:#7f8fa4;font-weight:400;font-size:11px;text-transform:uppercase;letter-spacing:1px;" title="Backend bugs (pytest.xfail) — if this drops, a bug was fixed">Known Bugs</th>
              <th style="padding:8px 12px;text-align:center;color:#7f8fa4;font-weight:400;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Pass %</th>
            </tr>
          </thead>
          <tbody style="color:#ecf0f1;">
{env_rows_html}
          </tbody>
        </table>
      </div>

      <!-- Note about execution order -->
      <div style="padding:12px 16px;background:#253545;border-radius:8px;border-left:4px solid #5dade2;margin-bottom:28px;">
        <p style="margin:0;font-size:12px;color:#85929e;">
          Environments ran <strong style="color:#ecf0f1;">sequentially</strong>: qa1 &rarr; stag &rarr; prod &rarr; china prod &rarr; china stag.
          Each environment continued regardless of the previous one's result.
          A failure in any environment marks the pipeline as <span style="color:#e74c3c;font-weight:600;">FAILED</span>.
          <br/><strong style="color:#f39c12;">Known Bugs</strong> are tests guarded by <code>pytest.xfail</code> against known backend bugs —
          if one suddenly passes, Allure will mark it <strong>XPASS</strong> so you know the bug is fixed and the guard can be removed.
        </p>
      </div>

      <!-- CTA -->
      <div style="text-align:center;margin-top:8px;">
        <table align="center" cellspacing="0" cellpadding="0">
          <tr>
            <td align="center" style="border-radius:6px;background:linear-gradient(135deg,#1b2a3b,#2c3e50);">
              <a href="{report_url}"
                 style="font-size:15px;font-family:Helvetica,Arial,sans-serif;color:#ffffff;
                        text-decoration:none;padding:13px 28px;display:inline-block;
                        font-weight:600;letter-spacing:0.5px;">
                View Full Allure Report &rarr;
              </a>
            </td>
          </tr>
        </table>
      </div>

    </div>

    <!-- Footer -->
    <div style="background-color:#0f1923;padding:14px;text-align:center;border-top:1px solid #253545;">
      <p style="font-size:11px;color:#5d6d7e;margin:0;">
        Generated by Azure DevOps &nbsp;&#124;&nbsp; Build #{build_id} &nbsp;&#124;&nbsp; {build_number}
      </p>
    </div>

  </div>
</div>"""


# ─────────────────────────────────────────────────────────────────────────────
# SMTP
# ─────────────────────────────────────────────────────────────────────────────

def send_email(
    recipient: str,
    subject: str,
    html_body: str,
    smtp_server: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    sender: str,
) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = sender
    msg["To"]      = recipient
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(sender, recipient, msg.as_string())


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()

    smtp_server   = os.environ.get("SMTP_SERVER", "")
    smtp_port_raw = os.environ.get("SMTP_PORT", "465")
    smtp_user     = os.environ.get("SMTP_USER", "")
    smtp_password = os.environ.get("SMTP_PASSWORD", "")
    sender        = os.environ.get("NOREPLY_EMAIL", "noreply@netafim.com")

    try:
        smtp_port = int(smtp_port_raw)
    except (ValueError, TypeError):
        print(f"[ERROR] SMTP_PORT is not a valid integer: {smtp_port_raw!r}", file=sys.stderr)
        sys.exit(1)

    if not all([smtp_server, smtp_user, smtp_password]):
        print("[ERROR] Missing SMTP environment variables. Email not sent.", file=sys.stderr)
        sys.exit(1)

    envs = load_env_stats(args.env_stats)
    agg  = aggregate(envs)

    html = build_html(
        envs=envs,
        agg=agg,
        build_id=args.build_id,
        build_number=args.build_number,
        report_url=args.report_url,
    )

    status_word = "FAILED" if agg["any_failure"] else "PASSED"
    subject = (
        f"[{status_word}] API Nightly Report - All Envs - "
        f"{agg['pass_pct']}% Passed (Build {args.build_id})"
    )

    recipients = [r.strip() for r in args.recipients.split(",") if r.strip()]
    errors = []
    for recipient in recipients:
        try:
            send_email(recipient, subject, html,
                       smtp_server, smtp_port, smtp_user, smtp_password, sender)
            print(f"[OK] Email sent to {recipient}")
        except Exception as exc:
            print(f"[ERROR] Failed to send to {recipient}: {exc}", file=sys.stderr)
            errors.append(recipient)

    if errors:
        print(f"[WARN] Failed to deliver to: {', '.join(errors)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
