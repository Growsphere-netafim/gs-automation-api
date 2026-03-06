#!/usr/bin/env python3
"""
Send a styled HTML nightly-test-report email via SMTP.
Called from pipelines/qa1/nightly-api-tests.yml after Allure report generation.

Usage:
    python3 scripts/send_report_email.py \
        --summary-json allure-report-local/widgets/summary.json \
        --env-name qa1 \
        --test-info nightly \
        --build-id 12345 \
        --build-number "20260220.1" \
        --report-url "https://..." \
        --recipients "a@x.com, b@x.com"

Required environment variables (set by Azure DevOps pipeline):
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


# ──────────────────────────────────────────────────────────────────
# Parse CLI args
# ──────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--summary-json",  default="allure-report-local/widgets/summary.json")
    p.add_argument("--env-name",      default="qa1")
    p.add_argument("--test-info",     default="nightly")
    p.add_argument("--build-id",      default="0")
    p.add_argument("--build-number",  default="")
    p.add_argument("--report-url",    default="")
    p.add_argument("--recipients",    required=True)
    return p.parse_args()


# ──────────────────────────────────────────────────────────────────
# Read Allure summary
# ──────────────────────────────────────────────────────────────────

def read_summary(path: str) -> dict:
    try:
        with open(path) as f:
            data = json.load(f)
        s       = data.get("statistic", {})
        total   = s.get("total",   0)
        passed  = s.get("passed",  0)
        failed  = s.get("failed",  0)
        broken  = s.get("broken",  0)
        skipped = s.get("skipped", 0)
    except Exception as e:
        print(f"[WARN] Could not read summary: {e}", file=sys.stderr)
        total = passed = failed = broken = skipped = 0

    pass_pct   = round(passed / total * 100, 2) if total > 0 else 0
    pass_width = int(round(passed  / total * 100)) if total > 0 else 0
    fail_width = int(round((failed + broken) / total * 100)) if total > 0 else 0

    if passed > 0 and pass_width == 0:
        pass_width = 1
    if (failed + broken) > 0 and fail_width == 0:
        fail_width = 1

    return dict(
        total=total, passed=passed, failed=failed,
        broken=broken, skipped=skipped,
        pass_pct=pass_pct,
        pass_width=pass_width, fail_width=fail_width,
    )


# ──────────────────────────────────────────────────────────────────
# Build HTML — identical layout to the web nightly email
# ──────────────────────────────────────────────────────────────────

def build_html(s: dict, env_name: str, test_info: str,
               build_id: str, build_number: str, report_url: str) -> str:

    total      = s["total"]
    passed     = s["passed"]
    failed     = s["failed"]
    broken     = s["broken"]
    skipped    = s["skipped"]
    pass_pct   = s["pass_pct"]
    pass_width = s["pass_width"]
    fail_width = s["fail_width"]

    # ── API email color palette (distinct from the Web automation email) ──
    # Web uses:  navy #0b1e33 header | lime #97cc64 pass | orange-red #fd5a3e fail | yellow #ffcc00 broken
    # API uses:  slate #1b2a3b header | emerald #2ecc71 pass | crimson #e74c3c fail | orange #e67e22 broken | blue-grey skipped

    return f"""<div style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #0f1923; padding: 28px;">
  <div style="background-color: #1b2838; max-width: 650px; margin: 0 auto; border-radius: 10px; overflow: hidden; box-shadow: 0 6px 24px rgba(0,0,0,0.5);">

    <!-- Header -->
    <div style="background: linear-gradient(135deg, #1b2a3b 0%, #2c3e50 100%); padding: 24px 20px; text-align: center;">
      <p style="color: #5dade2; margin: 0 0 6px 0; font-size: 11px; text-transform: uppercase; letter-spacing: 3px;">API Automation</p>
      <h2 style="color: #ffffff; margin: 0; font-weight: 600; font-size: 22px; letter-spacing: 0.5px;">Nightly Test Report</h2>
      <p style="color: #85929e; margin: 8px 0 0 0; font-size: 13px;">Env: {env_name} &nbsp;&#124;&nbsp; {test_info}</p>
    </div>

    <div style="padding: 32px 28px;">

      <!-- Pass % -->
      <div style="text-align: center; margin-bottom: 28px;">
        <h1 style="font-size: 52px; color: #ffffff; margin: 0; font-weight: 700; letter-spacing: -1px;">{pass_pct}%</h1>
        <span style="color: #7f8fa4; font-size: 13px; text-transform: uppercase; letter-spacing: 2px;">Success Rate</span>
      </div>

      <!-- Progress bar -->
      <div style="height: 10px; background-color: #253545; border-radius: 5px; overflow: hidden; display: flex; margin-bottom: 32px;">
        <div style="width: {pass_width}%; background: linear-gradient(90deg, #27ae60, #2ecc71);"></div>
        <div style="width: {fail_width}%; background: linear-gradient(90deg, #c0392b, #e74c3c);"></div>
      </div>

      <!-- Stats -->
      <table style="width: 100%; border-collapse: separate; border-spacing: 8px; margin-bottom: 4px;">
        <tr>
          <td style="background: #253545; padding: 16px 10px; border-radius: 8px; text-align: center; border-bottom: 3px solid #3d5166;">
            <div style="font-size: 26px; font-weight: 700; color: #ecf0f1;">{total}</div>
            <div style="font-size: 11px; color: #7f8fa4; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px;">Total Runs</div>
          </td>
          <td style="background: #1a3a2a; padding: 16px 10px; border-radius: 8px; text-align: center; border-bottom: 3px solid #2ecc71;">
            <div style="font-size: 26px; font-weight: 700; color: #2ecc71;">{passed}</div>
            <div style="font-size: 11px; color: #58d68d; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px;">Passed</div>
          </td>
          <td style="background: #3a1a1a; padding: 16px 10px; border-radius: 8px; text-align: center; border-bottom: 3px solid #e74c3c;">
            <div style="font-size: 26px; font-weight: 700; color: #e74c3c;">{failed}</div>
            <div style="font-size: 11px; color: #ec7063; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px;">Failed</div>
          </td>
          <td style="background: #3a2a10; padding: 16px 10px; border-radius: 8px; text-align: center; border-bottom: 3px solid #e67e22;">
            <div style="font-size: 26px; font-weight: 700; color: #e67e22;">{broken}</div>
            <div style="font-size: 11px; color: #f0a500; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px;">Broken</div>
          </td>
          <td style="background: #253545; padding: 16px 10px; border-radius: 8px; text-align: center; border-bottom: 3px solid #5d6d7e;">
            <div style="font-size: 26px; font-weight: 700; color: #85929e;">{skipped}</div>
            <div style="font-size: 11px; color: #7f8fa4; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px;">Skipped</div>
          </td>
        </tr>
      </table>

      <!-- API Coverage section -->
      <div style="margin-top: 24px; padding: 16px 18px; background: #253545; border-radius: 8px; border-left: 4px solid #5dade2;">
        <p style="margin: 0 0 12px 0; font-size: 11px; color: #5dade2; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;">API Test Coverage</p>
        <table style="width: 100%; font-size: 13px;">
          <tr>
            <td style="padding: 5px 0;">
              <span style="color: #2ecc71; font-size: 10px;">&#9632;</span>
              &nbsp;<strong style="color: #ecf0f1;">Integration Tests</strong>
            </td>
            <td style="text-align: right; color: #7f8fa4;">
              CSAPI &middot; FieldIO &middot; DataAPI &middot; Irrigation &middot; CropService &middot; Weather
            </td>
          </tr>
          <tr>
            <td style="padding: 5px 0;">
              <span style="color: #5dade2; font-size: 10px;">&#9632;</span>
              &nbsp;<strong style="color: #ecf0f1;">QA1 Deep Tests</strong>
            </td>
            <td style="text-align: right; color: #7f8fa4;">
              80+ endpoints across all microservices
            </td>
          </tr>
          <tr>
            <td style="padding: 5px 0;">
              <span style="color: #5d6d7e; font-size: 10px;">&#9632;</span>
              &nbsp;<span style="color: #7f8fa4;">Skipped</span>
            </td>
            <td style="text-align: right; color: #5d6d7e;">
              {skipped} tests &mdash; missing context (deviceId, cropUnitId, seasonId&hellip;)
            </td>
          </tr>
        </table>
        <p style="margin: 12px 0 0 0; font-size: 11px; color: #7f8fa4;">
          Skipped tests are <strong style="color: #ecf0f1;">not failures</strong> &mdash; the pipeline stays
          <span style="color: #2ecc71; font-weight: bold;">GREEN</span> for skipped tests.
        </p>
      </div>

      <!-- CTA button -->
      <div style="text-align: center; margin-top: 32px;">
        <table align="center" cellspacing="0" cellpadding="0">
          <tr>
            <td align="center" style="border-radius: 6px; background: linear-gradient(135deg, #1b2a3b, #2c3e50);">
              <a href="{report_url}"
                 style="font-size: 15px; font-family: Helvetica, Arial, sans-serif; color: #ffffff;
                        text-decoration: none; padding: 13px 28px; display: inline-block;
                        font-weight: 600; letter-spacing: 0.5px;">
                View Full Allure Report &rarr;
              </a>
            </td>
          </tr>
        </table>
      </div>

    </div>

    <!-- Footer -->
    <div style="background-color: #0f1923; padding: 14px; text-align: center; border-top: 1px solid #253545;">
      <p style="font-size: 11px; color: #5d6d7e; margin: 0;">
        Generated by Azure DevOps &nbsp;&#124;&nbsp; Build #{build_id} &nbsp;&#124;&nbsp; {build_number}
      </p>
    </div>

  </div>
</div>"""


# ──────────────────────────────────────────────────────────────────
# Send email
# ──────────────────────────────────────────────────────────────────

def send_email(recipient: str, subject: str, html_body: str,
               smtp_server: str, smtp_port: int,
               smtp_user: str, smtp_password: str, sender: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = sender
    msg["To"]      = recipient
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(sender, recipient, msg.as_string())


# ──────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    smtp_server   = os.environ.get("SMTP_SERVER", "")
    smtp_port     = int(os.environ.get("SMTP_PORT", "465"))
    smtp_user     = os.environ.get("SMTP_USER", "")
    smtp_password = os.environ.get("SMTP_PASSWORD", "")
    sender        = os.environ.get("NOREPLY_EMAIL", "noreply@netafim.com")

    if not all([smtp_server, smtp_user, smtp_password]):
        print("[ERROR] Missing SMTP environment variables. Email not sent.", file=sys.stderr)
        sys.exit(1)

    summary = read_summary(args.summary_json)
    html    = build_html(
        summary, args.env_name, args.test_info,
        args.build_id, args.build_number, args.report_url,
    )

    subject = (
        f"Nightly Report: {args.env_name} - "
        f"{summary['pass_pct']}% Passed (Build {args.build_id})"
    )

    recipients = [r.strip() for r in args.recipients.split(",") if r.strip()]
    errors = []

    for recipient in recipients:
        try:
            send_email(recipient, subject, html,
                       smtp_server, smtp_port, smtp_user, smtp_password, sender)
            print(f"[OK] Email sent to {recipient}")
        except Exception as e:
            print(f"[ERROR] Failed to send to {recipient}: {e}", file=sys.stderr)
            errors.append(recipient)

    if errors:
        print(f"\n[WARN] Failed to send to: {', '.join(errors)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
