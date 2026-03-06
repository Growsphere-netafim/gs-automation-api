import allure
import json
from typing import Any, Dict

def attach_json(data: Any, name: str):
    """Explicitly attach JSON data to Allure report."""
    allure.attach(
        json.dumps(data, indent=2),
        name=name,
        attachment_type=allure.attachment_type.JSON
    )


# ==================== Failure Diagnosis ====================

def analyze_get_failure(response) -> str:
    """
    Generate a detailed diagnostic report for a failed GET response.
    Explains: why it failed, what was returned, what the API needs, and recommendations.
    """
    method = response.request.method
    url = str(response.request.url)
    status = response.status_code

    lines = []
    lines.append("=" * 60)
    lines.append("FAILURE DIAGNOSIS")
    lines.append("=" * 60)
    lines.append(f"Method  : {method}")
    lines.append(f"URL     : {url}")
    lines.append(f"Status  : {status}")
    lines.append("")

    # --- Why it failed ---
    lines.append("WHY IT FAILED")
    lines.append("-" * 40)
    reasons = {
        400: "Bad Request – invalid or missing required parameters.",
        401: "Unauthorized – bearer token is missing, expired, or invalid.",
        403: "Forbidden – user lacks permission for this resource or farm.",
        404: "Not Found – the requested resource / ID does not exist.",
        405: "Method Not Allowed – this endpoint does not support GET.",
        408: "Request Timeout – server took too long to respond.",
        422: "Unprocessable Entity – correct format but invalid values.",
        429: "Too Many Requests – rate limit exceeded.",
        500: "Internal Server Error – crash or bug on the server side.",
        502: "Bad Gateway – upstream service is unavailable.",
        503: "Service Unavailable – service is down or overloaded.",
        504: "Gateway Timeout – upstream service timed out.",
    }
    lines.append(reasons.get(status, f"HTTP {status} – unexpected error."))
    lines.append("")

    # --- What was returned ---
    lines.append("WHAT WAS RETURNED")
    lines.append("-" * 40)
    try:
        body = response.json()
        error_detail = (
            body.get("error") or
            body.get("message") or
            body.get("Message") or
            body.get("errorMessage") or
            body.get("title") or
            body.get("detail") or
            body.get("Detail")
        )
        if error_detail:
            lines.append(f"Error Message : {error_detail}")
        if "errors" in body:
            lines.append(f"Validation    : {json.dumps(body['errors'])}")
        trace = body.get("traceId") or body.get("TraceId")
        if trace:
            lines.append(f"Trace ID      : {trace}")
        raw = json.dumps(body, indent=2)
        lines.append(f"Full Body:\n{raw[:2000]}")
    except Exception:
        text = response.text or "(empty body)"
        lines.append(f"Body (text): {text[:500]}")
    lines.append("")

    # --- What the API needs ---
    lines.append("WHAT THE API NEEDS TO WORK")
    lines.append("-" * 40)
    url_lower = url.lower()
    needs = ["* Authorization: Bearer <valid_token>  (required for all endpoints)"]

    if any(k in url_lower for k in ["farm", "cropunit", "block", "field", "zone", "plot"]):
        needs.append("* farmId – a valid active farm ID")
        needs.append("  -> Discover: GET https://csapi-qa1.k8s.growsphere.netafim.com/api/v1/farms")

    if any(k in url_lower for k in ["device", "sensor", "base", "heartbeat", "devicestate"]):
        needs.append("* deviceId / deviceUuid – a device linked to the farm")
        needs.append("  -> Discover: GET https://fieldio-qa1.k8s.growsphere.netafim.com/api/devices?farmId=<id>")

    if any(k in url_lower for k in ["history", "telemetry", "log", "heartbeat", "report", "recommendation", "forecast"]):
        needs.append("* fromDateTimeUtc + toDateTimeUtc – ISO 8601 date range")
        needs.append("  -> Example: fromDateTimeUtc=2024-01-01T00:00:00Z&toDateTimeUtc=2024-12-31T23:59:59Z")

    if any(k in url_lower for k in ["crop", "variety", "phenologic", "protocol"]):
        needs.append("* cropId / varietyId – from cropservice /api/Crops or /api/Varieties")

    if any(k in url_lower for k in ["irrigation", "irrigationunit", "program"]):
        needs.append("* irrigationUnitId / programId – from irrigation service list endpoints")

    if any(k in url_lower for k in ["command", "commandsmanager"]):
        needs.append("* deviceId + commandType – device must be online and reachable")

    lines.extend(needs)
    lines.append("")

    # --- Recommendations ---
    lines.append("RECOMMENDATIONS")
    lines.append("-" * 40)
    if status == 401:
        lines.append("[!] Token is expired or missing. Re-run with a fresh bearer token.")
        lines.append("[!] Check IDS_URL in config and confirm credentials are correct.")
        lines.append("[!] Run: python run_tests.py  (it will auto-fetch a new token)")
    elif status == 403:
        lines.append("[!] Use a user account with admin/manager permissions.")
        lines.append("[!] Verify the farmId belongs to the test user's account.")
        lines.append("[!] Try a different farm — this farm may have restricted access.")
    elif status == 404:
        lines.append("[!] Fetch a list first (e.g. /farms, /devices) and use a real ID from the list.")
        lines.append("[!] The resource may have been deleted or the ID is from a different environment.")
        lines.append("[!] Try switching to a different farmId or deviceId.")
    elif status == 400:
        lines.append("[!] Review required query parameters in the Swagger/OpenAPI spec.")
        lines.append("[!] Ensure all ID values are non-empty and in the correct format.")
        lines.append("[!] Check header requirements (x-nbvx-usr-pref-unit-system, x-gs-farm-timezone).")
    elif status >= 500:
        lines.append("[!] Check the k8s service health — may be a transient error.")
        lines.append("[!] Retry the test after a few minutes.")
        lines.append("[!] Inspect service logs on the cluster for the stack trace.")
    lines.append("=" * 60)

    return "\n".join(lines)


def attach_failure_diagnosis(response):
    """
    Attach a detailed failure diagnosis attachment to Allure for a failed GET request.
    Also prints the diagnosis to the console.
    """
    diagnosis = analyze_get_failure(response)
    status = response.status_code
    url = str(response.request.url)

    # Print to terminal so it appears in pytest -s output
    print(f"\n{diagnosis}")

    # Attach as a prominent, named section in Allure
    allure.attach(
        diagnosis,
        name=f"[FAILURE DIAGNOSIS] HTTP {status} — {url}",
        attachment_type=allure.attachment_type.TEXT
    )


def attach_empty_response_warning(response, context_hint: str = ""):
    """
    Attach a warning to Allure when an API returns 200 OK but with an empty body ([], {}, "").
    Provides recommendations for resolving the empty data issue.
    """
    url = str(response.request.url)

    lines = [
        "=" * 60,
        "EMPTY RESPONSE WARNING",
        "=" * 60,
        f"URL    : {url}",
        f"Status : {response.status_code} OK  (but returned empty data — no records found)",
        "",
        "POSSIBLE CAUSES",
        "-" * 40,
        "* The farmId has no associated records in this service",
        "* The device / sensor is not active or not configured",
        "* For time-series queries: the date range contains no events",
        "* The farm exists but has no crops / devices / irrigation units set up",
        "* The service filter excludes this farm's data (check headers)",
        "",
        "RECOMMENDATIONS",
        "-" * 40,
        "[!] Try a different farmId — one with active devices and data",
        "[!] Verify the farm is fully configured in Growsphere",
        "[!] For date-range queries: extend the range or use a recent period",
        "[!] Check that the test farm has been seeded with data",
        "[!] Confirm the correct unit system header: x-nbvx-usr-pref-unit-system: SI",
    ]

    if context_hint:
        lines.append(f"[!] {context_hint}")

    lines.append("=" * 60)
    warning_text = "\n".join(lines)

    print(f"\n{warning_text}")

    allure.attach(
        warning_text,
        name=f"[EMPTY RESPONSE] No data returned — {url}",
        attachment_type=allure.attachment_type.TEXT
    )


# ==================== Response Logger ====================

def log_response(response):
    """
    Log response details to Console (Pretty JSON) and Allure (Attachments).
    For failed GET requests, automatically attaches a detailed failure diagnosis.
    For empty GET responses (200 + []/{}), attaches an empty-response warning.
    """
    method = response.request.method
    url = response.request.url
    status = response.status_code

    # --- Console Output ---
    print(f"\n[API] {method} {url} -> {status}")

    # Try to parse JSON for pretty printing
    try:
        resp_json = response.json()
        formatted_json = json.dumps(resp_json, indent=2)
        print(formatted_json)
    except Exception:
        formatted_json = None
        if response.text and len(response.text) < 1000:
            print(response.text)

    # --- Allure Attachments ---
    step_name = f"{method} {url}"
    with allure.step(step_name):
        # 1. Request details
        req_info = (
            f"Method: {method}\n"
            f"URL: {url}\n"
            f"Headers: {json.dumps(dict(response.request.headers), indent=2)}"
        )
        allure.attach(req_info, name="Request Metadata", attachment_type=allure.attachment_type.TEXT)

        if response.request.body:
            body_str = response.request.body
            if isinstance(body_str, bytes):
                body_str = body_str.decode("utf-8", errors="ignore")
            allure.attach(body_str, name="Request Body", attachment_type=allure.attachment_type.JSON)

        # 2. Response details
        res_info = (
            f"Status: {status}\n"
            f"Elapsed: {response.elapsed}\n"
            f"Headers: {json.dumps(dict(response.headers), indent=2)}"
        )
        allure.attach(res_info, name="Response Metadata", attachment_type=allure.attachment_type.TEXT)

        if formatted_json:
            allure.attach(formatted_json, name="Response Body (JSON)", attachment_type=allure.attachment_type.JSON)
            if status >= 400:
                allure.attach(formatted_json, name=f"!!! FAILED ({status}) !!!", attachment_type=allure.attachment_type.JSON)
        else:
            allure.attach(response.text or "(empty)", name="Response Body (Text)", attachment_type=allure.attachment_type.TEXT)

        # 3. Failure diagnosis for all failed GET requests
        if method == "GET" and status >= 400:
            attach_failure_diagnosis(response)

        # 4. Empty response warning for GET 200 with no data
        elif method == "GET" and status == 200:
            try:
                body = response.json()
                if body == [] or body == {} or body == "":
                    attach_empty_response_warning(response)
                elif isinstance(body, dict):
                    # Check nested lists that are empty (e.g. {"deviceList": [], "total": 0})
                    for key, val in body.items():
                        if isinstance(val, list) and len(val) == 0:
                            attach_empty_response_warning(
                                response,
                                context_hint=f"Field '{key}' is an empty list inside the response object."
                            )
                            break
            except Exception:
                pass
