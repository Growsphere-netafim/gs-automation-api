#!/usr/bin/env python3
"""
Send a standalone OpenAPI schema-drift report by email.

Consumes the JSON written by scripts/detect_schema_drift.py and sends
a compact HTML summary showing endpoints that were added, removed, or
had their signature changed compared to the committed swagger_specs/
baseline.

This is intentionally decoupled from the main nightly email — it
ships only to a small audience (the automation owner and their
manager), not the broader QA list.

Usage:
    python3 scripts/send_schema_drift_email.py \
        --drift-json   reports/schema-drift.json \
        --build-id     "$(Build.BuildId)" \
        --build-number "$(Build.BuildNumber)" \
        --recipients   "a@x.com, b@x.com"

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


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Schema drift email sender")
    p.add_argument("--drift-json",   required=True)
    p.add_argument("--build-id",     default="0")
    p.add_argument("--build-number", default="")
    p.add_argument("--recipients",   required=True,
                   help="Comma-separated recipient list")
    return p.parse_args()


def _load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ─────────────────────────────────────────────────────────────────────────────
# HTML
# ─────────────────────────────────────────────────────────────────────────────


def _endpoint_rows(items: list, color: str) -> str:
    if not items:
        return ""
    rows = []
    for ep in items:
        method = ep.get("method", "")
        path   = ep.get("path", "")
        rows.append(f"""
          <tr>
            <td style="padding:4px 10px;color:{color};font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;width:60px;">{method}</td>
            <td style="padding:4px 10px;color:#ecf0f1;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;">{path}</td>
          </tr>""")
    return "\n".join(rows)


def _service_block(svc: dict) -> str:
    host      = svc.get("host", "")
    service   = svc.get("service", host)
    added     = svc.get("added", [])
    removed   = svc.get("removed", [])
    changed   = svc.get("changed", [])

    sections = []
    if added:
        sections.append(f"""
          <tr><td colspan="2" style="padding:10px 0 4px 0;color:#2ecc71;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;">+ Added ({len(added)})</td></tr>
          {_endpoint_rows(added, "#2ecc71")}""")
    if removed:
        sections.append(f"""
          <tr><td colspan="2" style="padding:10px 0 4px 0;color:#e74c3c;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;">- Removed ({len(removed)})</td></tr>
          {_endpoint_rows(removed, "#e74c3c")}""")
    if changed:
        sections.append(f"""
          <tr><td colspan="2" style="padding:10px 0 4px 0;color:#f39c12;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;">~ Changed signature ({len(changed)})</td></tr>
          {_endpoint_rows(changed, "#f39c12")}""")

    return f"""
      <div style="background:#1e2b37;border-radius:8px;padding:12px 16px;margin-bottom:14px;">
        <div style="color:#5dade2;font-size:13px;font-weight:600;margin-bottom:6px;">{service.upper()} <span style="color:#7f8fa4;font-weight:400;font-size:11px;">({host})</span></div>
        <table style="width:100%;border-collapse:collapse;">
          {"".join(sections)}
        </table>
      </div>"""


def build_html(drift: dict, build_id: str, build_number: str) -> str:
    summary = drift.get("summary", {}) or {}
    services = drift.get("services", []) or []
    offline = drift.get("offline", []) or []
    generated_at = drift.get("generated_at") or ""

    added_total   = int(summary.get("added", 0))
    removed_total = int(summary.get("removed", 0))
    changed_total = int(summary.get("changed", 0))
    drift_services_count = int(summary.get("services_with_drift", 0))

    any_drift = added_total + removed_total + changed_total > 0
    status_color = "#e67e22" if any_drift else "#1e8449"
    status_label = "SCHEMA DRIFT DETECTED" if any_drift else "NO DRIFT"

    services_html = "\n".join(_service_block(s) for s in services) if services else (
        '<div style="color:#85929e;padding:16px;background:#1e2b37;border-radius:8px;font-size:13px;">'
        'No endpoints added, removed, or changed since the committed baseline.'
        '</div>'
    )

    offline_html = ""
    if offline:
        offline_list = ", ".join(f'<code style="color:#ec7063;">{h}</code>' for h in offline)
        offline_html = f"""
        <div style="padding:12px 16px;background:#3a1a1a;border-radius:8px;border-left:4px solid #e74c3c;margin-top:14px;">
          <p style="margin:0;font-size:12px;color:#ec7063;">
            <strong>Services unreachable:</strong> {offline_list}<br/>
            <span style="color:#85929e;">Their baselines could not be compared this run. Check connectivity / URL.</span>
          </p>
        </div>"""

    return f"""<div style="font-family:'Segoe UI',Arial,sans-serif;background-color:#0f1923;padding:28px;">
  <div style="background-color:#1b2838;max-width:720px;margin:0 auto;border-radius:10px;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,0.5);">

    <div style="background:linear-gradient(135deg,#1b2a3b 0%,#2c3e50 100%);padding:22px 20px;text-align:center;">
      <p style="color:#5dade2;margin:0 0 6px 0;font-size:11px;text-transform:uppercase;letter-spacing:3px;">API Automation</p>
      <h2 style="color:#ffffff;margin:0;font-weight:600;font-size:20px;letter-spacing:0.5px;">OpenAPI Schema Drift Report</h2>
      <p style="color:#85929e;margin:8px 0 0 0;font-size:12px;">Diff vs committed <code>swagger_specs/</code> baseline</p>
      <div style="margin-top:10px;">
        <span style="background:{status_color};color:#fff;padding:3px 12px;border-radius:12px;font-size:12px;font-weight:700;letter-spacing:1px;">{status_label}</span>
      </div>
    </div>

    <div style="padding:28px 24px;">

      <table style="width:100%;border-collapse:separate;border-spacing:8px;margin-bottom:24px;">
        <tr>
          <td style="background:#1a3a2a;padding:14px 10px;border-radius:8px;text-align:center;border-bottom:3px solid #2ecc71;">
            <div style="font-size:24px;font-weight:700;color:#2ecc71;">{added_total}</div>
            <div style="font-size:11px;color:#58d68d;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Added</div>
          </td>
          <td style="background:#3a1a1a;padding:14px 10px;border-radius:8px;text-align:center;border-bottom:3px solid #e74c3c;">
            <div style="font-size:24px;font-weight:700;color:#e74c3c;">{removed_total}</div>
            <div style="font-size:11px;color:#ec7063;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Removed</div>
          </td>
          <td style="background:#3a2d14;padding:14px 10px;border-radius:8px;text-align:center;border-bottom:3px solid #f39c12;">
            <div style="font-size:24px;font-weight:700;color:#f39c12;">{changed_total}</div>
            <div style="font-size:11px;color:#f39c12;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Changed</div>
          </td>
          <td style="background:#253545;padding:14px 10px;border-radius:8px;text-align:center;border-bottom:3px solid #5d6d7e;">
            <div style="font-size:24px;font-weight:700;color:#85929e;">{drift_services_count}</div>
            <div style="font-size:11px;color:#7f8fa4;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Services</div>
          </td>
        </tr>
      </table>

      {services_html}

      {offline_html}

      <div style="padding:12px 16px;background:#253545;border-radius:8px;border-left:4px solid #5dade2;margin-top:18px;">
        <p style="margin:0;font-size:12px;color:#85929e;">
          <strong style="color:#ecf0f1;">How to act:</strong><br/>
          &bull; <strong style="color:#2ecc71;">Added</strong> — consider writing a test for the new endpoint.<br/>
          &bull; <strong style="color:#e74c3c;">Removed</strong> — check if any existing test still references it.<br/>
          &bull; <strong style="color:#f39c12;">Changed</strong> — parameters / response codes / body schema were modified; existing tests may need an update.<br/>
          <br/>
          To accept and baseline these changes, run <code>python fetch_swagger_specs.py</code> locally and commit the updated <code>swagger_specs/</code> files.
        </p>
      </div>

    </div>

    <div style="background-color:#0f1923;padding:14px;text-align:center;border-top:1px solid #253545;">
      <p style="font-size:11px;color:#5d6d7e;margin:0;">
        Generated by Azure DevOps &nbsp;&#124;&nbsp; Build #{build_id} &nbsp;&#124;&nbsp; {build_number} &nbsp;&#124;&nbsp; {generated_at}
      </p>
    </div>

  </div>
</div>"""


# ─────────────────────────────────────────────────────────────────────────────
# SMTP
# ─────────────────────────────────────────────────────────────────────────────


def send_email(recipient: str, subject: str, html_body: str,
               smtp_server: str, smtp_port: int, smtp_user: str,
               smtp_password: str, sender: str) -> None:
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

    try:
        drift = _load(args.drift_json)
    except Exception as exc:
        print(f"[ERROR] Cannot read drift JSON at {args.drift_json!r}: {exc}", file=sys.stderr)
        sys.exit(1)

    summary = drift.get("summary", {}) or {}
    added   = int(summary.get("added", 0))
    removed = int(summary.get("removed", 0))
    changed = int(summary.get("changed", 0))
    status_word = "DRIFT" if (added + removed + changed) > 0 else "CLEAN"

    subject = (
        f"[{status_word}] OpenAPI Schema Drift Report - "
        f"+{added} / -{removed} / ~{changed} (Build {args.build_id})"
    )

    html = build_html(drift, args.build_id, args.build_number)

    recipients = [r.strip() for r in args.recipients.split(",") if r.strip()]
    if not recipients:
        print("[ERROR] No recipients given.", file=sys.stderr)
        sys.exit(1)

    errors = []
    for recipient in recipients:
        try:
            send_email(recipient, subject, html,
                       smtp_server, smtp_port, smtp_user, smtp_password, sender)
            print(f"[OK] Drift email sent to {recipient}")
        except Exception as exc:
            print(f"[ERROR] Failed to send drift email to {recipient}: {exc}", file=sys.stderr)
            errors.append(recipient)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
